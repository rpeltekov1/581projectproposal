import {z} from 'zod';
export const roomSchema=z.object({id:z.string().min(1).max(50),name:z.string().min(1).max(100),type:z.enum(['bedroom','bathroom','kitchen','living','hall','other']),area:z.number().nonnegative().max(100000).nullable()});
export const layoutSchema=z.object({unit:z.enum(['sqft','sqm']),area_basis:z.enum(['internal','gross','unknown']),total_area:z.number().positive().max(1000000).nullable(),bedrooms:z.number().int().min(0).max(100).nullable(),bathrooms:z.number().min(0).max(100).multipleOf(.5).nullable(),doors:z.number().int().min(0).max(1000).nullable(),windows:z.number().int().min(0).max(1000).nullable(),rooms:z.array(roomSchema).max(200),warnings:z.array(z.string().max(1000)).max(50)}).superRefine((v,ctx)=>{if(new Set(v.rooms.map(r=>r.id)).size!==v.rooms.length)ctx.addIssue({code:'custom',message:'Room IDs must be unique'});});
export type Layout=z.infer<typeof layoutSchema>;
export const blankLayout:Layout={unit:'sqft',area_basis:'unknown',total_area:null,bedrooms:null,bathrooms:null,doors:null,windows:null,rooms:[],warnings:[]};
export const demoKey:Layout={unit:'sqft',area_basis:'internal',total_area:960,bedrooms:2,bathrooms:1,doors:7,windows:6,rooms:[{id:'r1',name:'Living room',type:'living',area:280},{id:'r2',name:'Kitchen',type:'kitchen',area:160},{id:'r3',name:'Bedroom 1',type:'bedroom',area:180},{id:'r4',name:'Bedroom 2',type:'bedroom',area:160},{id:'r5',name:'Bathroom',type:'bathroom',area:80},{id:'r6',name:'Hall',type:'hall',area:100}],warnings:[]};
export const demoResult:Layout={...demoKey,doors:6,windows:5,total_area:945,rooms:demoKey.rooms.map(r=>({...r,area:r.id==='r1'?265:r.area})),warnings:['Demonstration result: deliberately includes errors. No AI extraction was run.']};
export function scoreLayout(raw:Layout,key:Layout){
 const counts=['bedrooms','bathrooms','doors','windows'] as const;
 const fields=counts.filter(k=>key[k]!==null).map(k=>({field:k,expected:key[k],actual:raw[k],correct:raw[k]===key[k]}));
 const factor=(u:string)=>u==='sqm'?10.76391041671:1;
 const area=(a:number|null,b:number|null)=>a===null||b===null?null:Math.abs(a*factor(raw.unit)-b*factor(key.unit))/(b*factor(key.unit)||1);
 const basisMatch=raw.area_basis===key.area_basis&&key.area_basis!=='unknown';
 const totalError=basisMatch?area(raw.total_area,key.total_area):null;
 const roomFields=key.rooms.map(r=>{const p=raw.rooms.find(p=>p.id===r.id);return {id:r.id,name:r.name,matched:!!p,typeCorrect:p?.type===r.type,areaError:p?area(p.area,r.area):null};});
 const correct=fields.filter(f=>f.correct).length;
 return {metric_version:'exact-count-relative-area-v1',count_accuracy:fields.length?correct/fields.length:null,count_fields:fields,total_area_relative_error:totalError,area_basis_match:basisMatch,room_recall:key.rooms.length?roomFields.filter(r=>r.matched).length/key.rooms.length:null,extra_rooms:raw.rooms.filter(r=>!key.rooms.some(k=>k.id===r.id)).length,room_fields:roomFields,note:'Room matching uses stable IDs. Align IDs before scoring untagged plans. Unknowns are not correct; areas require a matching declared basis.'};
}
