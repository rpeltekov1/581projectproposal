import type {Metadata} from 'next';
import './globals.css';
export const metadata:Metadata={title:'Parcel | Property & Floor-Plan Intelligence',description:'Explore properties, review floor-plan extractions, and track versioned accuracy.',icons:{icon:'/favicon.svg'}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
