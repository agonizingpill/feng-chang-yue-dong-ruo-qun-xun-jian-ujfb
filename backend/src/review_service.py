from datetime import datetime
from sqlalchemy import select
from fastapi import HTTPException
from .models import Hive,Visit,CareAction
from .review_models import ScreenReview
from .yard_service import require,audit,latest

def request(db,body,user):
    visit=require(db,Visit,body.visit_id,True);hive=require(db,Hive,visit.hive_id,True)
    existing=db.scalar(select(ScreenReview).where(ScreenReview.visit_id==visit.id).with_for_update())
    if existing:
        if existing.requested_by==user.email:return existing
        if existing.state=='pending':raise HTTPException(409,'该巡检已在复判中，等待另一名主管裁决，请勿重复申请')
        raise HTTPException(409,'该巡检已有复判结论，原结论继续有效，仅供查阅')
    if latest(db,hive.id)!=visit.id:raise HTTPException(409,'该箱已有更新巡检，旧巡检裁决仅供查阅，请基于最新巡检办理')
    if visit.anomaly_score is None or visit.status not in ['screened','needs_requeen']:
        raise HTTPException(409,'须先完成该巡检筛查，且仍在可处置状态，才能申请复判')
    if not visit.anomaly_flag:raise HTTPException(409,'该巡检未提示异常，无需复判')
    active=db.scalar(select(CareAction.id).where(CareAction.visit_id==visit.id,CareAction.kind=='feed',CareAction.status.in_(['planned','executed','rechecked'])))
    if active:raise HTTPException(409,'该巡检饲喂单已先办成，复判申请不再受理')
    row=ScreenReview(visit_id=visit.id,reason=body.reason,requested_by=user.email,original_score=visit.anomaly_score,original_flag=bool(visit.anomaly_flag),original_threshold=(visit.model_evidence or {}).get('threshold'),state='pending')
    db.add(row);audit(db,user,f'申请筛查复判 {visit.code} 原异常分值{visit.anomaly_score:.4f}');db.commit();return row

def decide(db,key,body,user):
    ref=require(db,ScreenReview,key);visit=require(db,Visit,ref.visit_id,True);hive=require(db,Hive,visit.hive_id,True);row=require(db,ScreenReview,key,True)
    if row.state!='pending':
        if row.state==body.decision:return row
        raise HTTPException(409,'该复判已有裁决，结论已冻结，不能更改')
    if row.requested_by==user.email:raise HTTPException(409,'须由另一名主管维持或撤销告警')
    row.state=body.decision;row.decision_note=body.note;row.decided_by=user.email;row.decided_at=datetime.utcnow()
    row.superseded=latest(db,hive.id)!=visit.id
    if body.decision=='revoked' and not row.superseded and hive.care_state in ['needs_care','observe']:
        hive.care_state='observe' if visit.queen_seen else 'needs_care'
    audit(db,user,f"复判{row.id} {visit.code} {'维持告警' if body.decision=='upheld' else '确认误报'}{'（旧单仅供查阅）' if row.superseded else ''}，原分值{row.original_score:.4f}保留")
    db.commit();return row
