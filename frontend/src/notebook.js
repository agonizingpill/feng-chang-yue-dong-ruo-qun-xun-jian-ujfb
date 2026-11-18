import {api} from './api.js';
export const book={hives:[],visits:[],care:[],lots:[],issues:[],queens:[],moves:[],insulationLots:[],installs:[],spring:[],reviews:[],selectedHive:31,selectedVisit:null,selectedCare:null,reviewVisit:null,planning:false,showAll:false};
export async function openNotebook(){[book.hives,book.visits,book.care,book.lots,book.issues,book.queens,book.moves,book.insulationLots,book.installs,book.spring,book.reviews]=await Promise.all([api('/hives'),api('/visits'),api('/care'),api('/feed-lots'),api('/feed-issues'),api('/queen-observations'),api('/moves'),api('/insulation-lots'),api('/insulation-installs'),api('/spring-reviews'),api('/screen-reviews')]);}
export const reviewOf=visitId=>book.reviews.find(r=>r.visit_id===visitId);
export function latestVisits(){const found=new Map();for(const visit of book.visits)if(!found.has(visit.hive_id))found.set(visit.hive_id,visit);return [...found.values()];}
