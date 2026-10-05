'use client';
import {useEffect,useRef} from 'react';
import type {Chart} from 'chart.js';
export default function DataChart({labels,values,label,percent=false}:{labels:string[];values:(number|null)[];label:string;percent?:boolean}){
 const canvas=useRef<HTMLCanvasElement>(null);
 useEffect(()=>{
  let chart:Chart|undefined,active=true;
  import('chart.js/auto').then(({default:Chart})=>{
   if(!active||!canvas.current)return;
   chart=new Chart(canvas.current,{
    type:'line',data:{labels,datasets:[{label,data:values,borderColor:'#277d58',backgroundColor:'#277d5812',fill:true,tension:.3,pointRadius:3,pointHoverRadius:6,borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{
     x:{grid:{display:false},ticks:{color:'#849187',font:{size:11}}},
     y:{min:percent?0:undefined,max:percent?100:undefined,grid:{color:'#eef2ef'},border:{display:false},ticks:{font:{size:11},color:'#849187',callback:value=>percent?`${value}%`:`$${value}M`}}
    }}
   });
  });
  return()=>{active=false;chart?.destroy()};
 },[JSON.stringify(labels),JSON.stringify(values),label,percent]);
 return <div className="chart"><canvas ref={canvas} role="img" aria-label={`${label}: ${values.map((v,i)=>`${labels[i]} ${v??'not scored'}`).join(', ')}`}/></div>
}
