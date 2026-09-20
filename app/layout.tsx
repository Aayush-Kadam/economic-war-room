import type { Metadata } from "next";
import "./globals.css";
export const metadata:Metadata={title:"Economic War Room — Monetary Policy Under Fire",description:"A historical central-banking decision laboratory created by Aayush Kadam.",openGraph:{title:"Economic War Room",description:"Make the decision first. Let history speak second.",images:[{url:"/og.png",width:1672,height:941,alt:"Economic War Room — Monetary Policy Under Fire"}]},twitter:{card:"summary_large_image",title:"Economic War Room",description:"Make the decision first. Let history speak second.",images:["/og.png"]}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
