import spec from "@/engine/unified_spec.json";

export type UnifiedInput={inflation:number;output:number;unemployment:number;stress:number;rate:number;baseline:number;guidance:string;seed:number};
function rng(seed:number){return()=>{let t=seed+=0x6D2B79F5;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
function normal(r:()=>number){const u=Math.max(r(),1e-9),v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function kernel(peak:number,magnitude:number){const raw=Array.from({length:spec.transmission.months},(_,h)=>h===0?0:(h/peak)*Math.exp(1-h/peak));const scale=Math.max(...raw);return raw.map(x=>magnitude*x/scale)}
function response(deviationBp:number[],name:"inflation"|"output"|"unemployment"|"financial_conditions"){
 const c=spec.transmission[name],k=kernel(c.peak_month,c.magnitude_per_100bp);
 return deviationBp.map((_,t)=>deviationBp.slice(0,t+1).reduce((a,d,j)=>a+d/100*k[t-j],0));
}
export function deterministicUnified(input:UnifiedInput,months=24){
 const changes=Array(12).fill(input.inflation/12),player=Array(months).fill(input.rate),base=Array(months).fill(input.baseline),dev=player.map((x,i)=>(x-base[i])*100);
 const ri=response(dev,"inflation"),ro=response(dev,"output"),ru=response(dev,"unemployment"),rs=response(dev,"financial_conditions");let y=input.output,u=input.unemployment,s=input.stress;
 return player.map((rate,t)=>{const flow=spec.inflation.intercept+spec.inflation.lag_coefficients.reduce((a,b,j)=>a+b*changes[changes.length-j-1],0)+ri[t]/12;changes.push(flow);y=spec.state.output_persistence*y+ro[t];u=4+spec.state.unemployment_persistence*(u-4)+ru[t];s=spec.state.stress_persistence*s+rs[t];return{month:t+1,pi:changes.slice(-12).reduce((a,b)=>a+b,0),y,u:Math.max(2.5,Math.min(12,u)),stress:Math.max(0,Math.min(2,s)),rate,deviationBp:dev[t]}})
}
export function simulateUnified(input:UnifiedInput,paths=1000){const r=rng(input.seed),series=Array.from({length:paths},()=>deterministicUnified(input).map(x=>({...x,pi:x.pi+normal(r)*.09,y:x.y+normal(r)*.08,u:x.u+normal(r)*.04})));const q=(h:number,k:"pi"|"y"|"u",p:number)=>series.map(x=>x[h][k]).sort((a,b)=>a-b)[Math.floor((paths-1)*p)];return [2,5,8,11,14,17,20,23].map(h=>({h,pi:q(h,"pi",.5),lo:q(h,"pi",.1),hi:q(h,"pi",.9),y:q(h,"y",.5),u:q(h,"u",.5)}))}
