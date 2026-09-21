export type SharedSpec=Record<string,any>;
export type InteractiveInput={monthlyPriceChanges:number[];output:number;unemployment:number;stress:number;rate:number;baseline:number;guidance:string;seed:number};
export function simulateUnified(spec:SharedSpec,input:InteractiveInput,paths?:number):Array<{h:number;pi:number;lo:number;hi:number;y:number;u:number}>;
export function deterministicUnified(spec:SharedSpec,input:Record<string,any>,months?:number,shockSequence?:Array<Record<string,number>>):Array<Record<string,number>>;
