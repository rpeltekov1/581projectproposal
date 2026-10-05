export type Property={id:number;title:string;price:number;bedrooms:number;bathrooms:number;sqft:number;latitude:number;longitude:number;status:string;neighborhood:string;type:string;days:number;agent:string;source?:string};
export const properties:Property[]=[
{id:1,title:'1847 Pine Street',price:1245000,bedrooms:3,bathrooms:2,sqft:1680,latitude:37.7885,longitude:-122.4256,status:'Active',neighborhood:'Pacific Heights',type:'Condominium',days:8,agent:'Alex Morgan'},
{id:2,title:'726 Hayes Street',price:895000,bedrooms:2,bathrooms:1,sqft:1120,latitude:37.7768,longitude:-122.4289,status:'Active',neighborhood:'Hayes Valley',type:'Condominium',days:12,agent:'Jamie Chen'},
{id:3,title:'3214 Washington Street',price:1895000,bedrooms:4,bathrooms:3,sqft:2460,latitude:37.7908,longitude:-122.4462,status:'Active',neighborhood:'Presidio Heights',type:'Single-family',days:5,agent:'Alex Morgan'},
{id:4,title:'950 Guerrero Street',price:1395000,bedrooms:3,bathrooms:2,sqft:1750,latitude:37.7558,longitude:-122.4238,status:'Active',neighborhood:'Noe Valley',type:'Single-family',days:18,agent:'Taylor Reed'},
{id:5,title:'1460 Sutter Street',price:725000,bedrooms:1,bathrooms:1,sqft:810,latitude:37.788,longitude:-122.423,status:'Active',neighborhood:'Lower Pacific Heights',type:'Condominium',days:24,agent:'Jamie Chen'},
{id:6,title:'2390 California Street',price:1595000,bedrooms:3,bathrooms:2.5,sqft:2050,latitude:37.7894,longitude:-122.4339,status:'Pending',neighborhood:'Pacific Heights',type:'Condominium',days:16,agent:'Taylor Reed'},
{id:7,title:'1158 Stanyan Street',price:1745000,bedrooms:4,bathrooms:2,sqft:2250,latitude:37.762,longitude:-122.453,status:'Active',neighborhood:'Cole Valley',type:'Single-family',days:7,agent:'Alex Morgan'},
{id:8,title:'478 Duboce Avenue',price:1045000,bedrooms:2,bathrooms:2,sqft:1280,latitude:37.769,longitude:-122.4304,status:'Active',neighborhood:'Duboce Triangle',type:'Condominium',days:11,agent:'Jamie Chen'},
{id:9,title:'2200 Jackson Street',price:2245000,bedrooms:4,bathrooms:3.5,sqft:2810,latitude:37.7928,longitude:-122.4326,status:'Active',neighborhood:'Pacific Heights',type:'Single-family',days:9,agent:'Taylor Reed'},
{id:10,title:'675 9th Avenue',price:1195000,bedrooms:3,bathrooms:2,sqft:1580,latitude:37.7768,longitude:-122.4672,status:'Sold',neighborhood:'Inner Richmond',type:'Single-family',days:22,agent:'Alex Morgan'},
{id:11,title:'1540 Lombard Street',price:985000,bedrooms:2,bathrooms:1,sqft:1190,latitude:37.801,longitude:-122.428,status:'Active',neighborhood:'Marina District',type:'Condominium',days:14,agent:'Jamie Chen'},
{id:12,title:'4020 18th Street',price:1475000,bedrooms:3,bathrooms:2,sqft:1830,latitude:37.7611,longitude:-122.4332,status:'Active',neighborhood:'Castro',type:'Condominium',days:6,agent:'Taylor Reed'}];
export const compact=(n:number)=>n>=1000000?`$${(n/1000000).toFixed(2).replace(/0$/,'')}M`:`$${Math.round(n/1000)}K`;
export const money=(n:number)=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
