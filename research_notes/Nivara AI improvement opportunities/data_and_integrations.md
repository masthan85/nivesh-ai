# Licensed Data Sources and Integration Options for Nivara AI (India, Nov 2026)

Research method note: done 25 Nov 2026 using web search only. Direct page fetches failed because this session's network blocks nsearchives.nseindia.com and casparser.in, so NSE PDF figures come from search-engine extracts of those PDFs and could not be read line by line. Every price below needs confirming with the vendor before anyone signs anything. Where a source date is known it is given. Training-knowledge items that I could not source are kept in Inferences or Gaps and labelled as unverified.

## 1. Licensed market data for NSE/BSE equities, indices, derivatives and ETFs

### Takeaway
NSE is the legal owner of its market data, and NSE Data & Analytics (NSE D&A) is the entity that licenses it. Any public display in a consumer app, even 15-minute delayed data, needs either a direct NSE D&A licence or a sublicence through an authorised vendor. Direct real-time licences cost in the tens of lakhs of rupees a year. The 15-minute-delayed capital-market tariff, which does not change for longer delays, is around ₹90,000 a year. For an early-stage app, the cheapest compliant path is delayed or EOD data through an authorised vendor such as TrueData, CMOTS or Accord, or through an authorised vendor's display licence. Self-licensing real-time data from NSE only makes sense at scale.

### Cited Findings
- NSE's Data Sharing & Usage Policy says NSE owns the data and authorises NSE Data (NSE D&A) to distribute it. It also says trading members and subscribers "shall not be permitted to redistribute any Market Data, except as agreed in the Relevant Agreement". This is why broker-API data cannot be redisplayed publicly without permission. — [NSE Data Sharing & Usage Policy](https://www.nseindia.com/static/market-data/nse-data-policy); [PDF](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/NSE_Data_Sharing&Usage_Policy.pdf)
- NSE's current market-data price list applies to NSE market data products effective 1 April 2026. Separate domestic and international PDFs were published in March 2026. I could not read the per-terminal, per-user and mobile-app lines because the fetch was blocked and the search extract was garbled. — [NSE Pricing file – Domestic clients (Mar 2026)](https://nsearchives.nseindia.com//web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf); [International](https://nsearchives.nseindia.com//web/mediaattachment/2026-03/NSE_Pricing_file_-_International_clients_20260309171502.pdf); [NSE Data & Info Vending page](https://www.nseindia.com/static/nse-data-and-analytics/data-information-vending)
- 15-minute delayed data tariff (undated NSE sheet): ₹90,000 a year domestic for the Capital Market segment. Commercials are the same for any delay of 15 minutes or more (20 min, 30 min, 1 hour). Real-time vendors may show delayed data on their own terminals or software at no extra fee, for display only. Delivering delayed data as a feed to a vendor's clients needs written consent from NSE D&A. — [NSE 15-min delayed data tariff](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Download%2015%20mins%20delayed%20data%20tariff.pdf)
- Real-time domestic tariff effective 1 Apr 2025, likely superseded by the Apr 2026 list: Capital Market terminal fixed fee of ₹24,00,000 a year. Mobile-app terms were 10% revenue share with a minimum of ₹11.5 lakh a year for paid apps, and ₹22,00,000 for free apps. The table's column order was ambiguous in the extract, so treat per-user figures as unreliable. — [NSE Real Time Tariff Domestic 01-04-2025](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Real_Time_Tariff_Domestic_01042025_.pdf)
- If the same data is taken directly and also through more vendors, the second and later sources are charged at 50% of the rate. — [NSE Real Time Tariff Domestic 2025](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Real_Time_Tariff_Domestic_01042025_.pdf)
- A secondary source (checked 13 Oct 2026, citing the 1 Apr 2026 price list) gives a Capital Market real-time snapshot fee of ₹29,20,000 a year per website, and ₹25,50,000 a year plus ₹875 per domestic user per month for a licensed charting application. Neither figure is verified against NSE's PDF. — [onetradejournal – why market data is delayed](https://onetradejournal.com/platforms/why-market-data-is-delayed)
- NSE real-time index products (older "other products" tariff): Nifty 50 real-time index at about ₹2,50,000 a year and a single stock at ₹10,000 a year. NSE notes that customers can take the data through an authorised data vendor. — [NSE real-time data subscription page](https://www.nseindia.com/static/market-data/real-time-data-subscription); [Other Products Tariff (Apr 2024)](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Download%20Other%20Products%20Tariff%20%28Effective%20April%2001%202024%29_7.pdf)
- NSE publishes a separate End-of-Day data tariff and a non-display licence document. Their amounts were not extractable. — [NSE EOD tariff](https://nsearchives.nseindia.com/s3fs-public/inline-files/Download%20EOD%20data%20tariff.pdf); [NSE D&A Non-display](https://archives.nseindia.com/content/press/Non_display.pdf)
- BSE India publishes a domestic "Information Products" tariff sheet covering real-time and delayed feeds for indices, equities, derivatives, debt, currency and commodities, priced per location and entity in INR and USD. It applies whether data comes directly from BSE or from BSE vendors in India. I could not extract the amounts. — [BSE Information Products Domestic Tariff Sheet](https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf)
- TrueData: Velocity (desktop) plans do not include API access. API access needs a separate application and approval, and pricing depends on exchange (NSE/BSE/MCX), symbol count and data type (streaming, charting, corporate). Exchange data fees are separate from TrueData's own pricing. — [TrueData pricing](https://www.truedata.in/information/pricing); [TrueData market data APIs](https://www.truedata.in/market-data-apis)
- TrueData plans bundled through Fyers, for Fyers clients only and undated: Level-1 real-time tick API at ₹1,599 a month plus GST, historical API at ₹1,599, and both together at ₹2,599. These are personal-use plans, not redistribution licences. — [Fyers community: Fyers ties up with TrueData](https://community.fyers.in/post/fyers-ties-up-with-truedata-5f40dc9ca9f2036c40234384)
- Global Datafeeds API pricing is quote-only. Global Financial Datafeeds LLP is on NSE's authorised-vendor list. — [onetradejournal – real time market data cost](https://onetradejournal.com/trading-apis/real-time-market-data-cost)
- A TradingView retail add-on for BSE real-time costs ₹422 a month for non-professionals and ₹3,705 for professionals. This is a per-user charting add-on, not a vendor feed fee. — [marketintelligencetools – market data pricing 2026](https://marketintelligencetools.com/reports/market-data-pricing/)

### Inferences
- A consumer app that shows NSE prices needs a display licence even for delayed data. Using yfinance or broker APIs as the public display source is non-compliant. Broker APIs are licensed to the individual account holder, and NSE's policy bars redistribution.
- The cheapest compliant phase-1 option is likely a vendor's 15-min-delayed or EOD display sublicence (TrueData, CMOTS, Accord, Global Datafeeds). The vendor holds the NSE agreement, and Nivara pays the vendor's fee plus any pass-through exchange fee. Using NSE's ₹90k delayed CM tariff as a floor, plus F&O, indices and BSE plus the vendor's margin, ₹2 to 6 lakh a year is a plausible order of magnitude for delayed display. This is an unverified estimate.
- Real-time display for a free app could cost ₹20 to 30 lakh a year or more in NSE fees alone, per the 2025 tariff and the 2026 secondary figure, before per-user fees. That is not justified for a beta of a few thousand users.
- From training knowledge, unverified here: Refinitiv/LSEG, Bloomberg and ICE are enterprise feeds priced per terminal or per enterprise licence, usually far above Indian vendor pricing, and they are not a fit for an early consumer app. Accelpix is understood to be an authorised NSE/BSE data vendor offering APIs for fintechs, but I did not confirm this.

### Gaps
- Exact 1 Apr 2026 NSE per-user, mobile-app and website fees, because the PDF was blocked. Fetch the domestic PDF directly, or ask NSE D&A (marketdata@nse.co.in, per NSE's vending page) for a quote.
- BSE vendor fee amounts, and Accelpix and Global Datafeeds quotes.
- Refinitiv/LSEG, Bloomberg and ICE India pricing: no public sources found.
- Whether NSE's derivatives and ETF delayed tariffs differ from the CM ₹90k figure. Only the CM line was surfaced.

## 2. Fundamentals, corporate actions, shareholding, filings and news

### Takeaway
The realistic licensed sources for Indian fundamentals plus corporate actions are CMOTS (API/JSON, 12-month basket subscription, mandatory "Data Powered by C-MOTS INFOTECH" attribution) and Accord Fintech (Datafeed over FTP or API; the Ace Equity Nxt research product starts at ₹1.25 lakh a year for a single user, which is not a redistribution licence). Neither publishes API prices. Scraping NSE or BSE is expressly prohibited by NSE's Terms of Use. I found no public pricing for news syndication from PTI, Reuters, ET or Moneycontrol.

### Cited Findings
- CMOTS offers APIs for equities, mutual funds, company announcements, commodities, currency, news, IPOs and derivatives, in delayed, historical and EOD frequencies, with "company fundamental information" across asset classes. — [CMOTS API datafeed](https://www.cmots.com/products/api-datafeed); [CMOTS market data provider](https://www.cmots.com/services/market-data-provider)
- CMOTS terms: data comes as JSON or XML, with CSV over FTP. Subscriptions run 12 months and charges vary by basket. One month's written notice is needed to stop renewal. Clients must display "Data Powered by C-MOTS INFOTECH" on output. Payment is in INR. — [APIDataFeed (CMOTS) Terms of Use](https://www.apidatafeed.com/terms-of-use); [CMOTS](https://www.cmots.com/)
- CMOTS was founded in 1997 in Mumbai and is unfunded. — [Tracxn – C-MOTS Infotech](https://tracxn.com/d/companies/cmots-infotech/__KXgCMqPDl7PUoHa6d9RLap1S4Rmdgv3RhG2LGaFY0BA)
- Ace Equity Nxt (Accord Fintech) covers 40,000+ companies (about 7,000 listed) with 1,750 annual-report fields. The basic annual subscription starts at ₹1,25,000 or USD 3,500 plus taxes. Accord separately sells datafeeds over FTP and API. — [Ace Equity Nxt subscribe](https://www.aceequitynxt.com/subscribe-now); [Accord ACE Equity Nxt](https://www.accordfintech.com/ace-equity-nxt); [Accord corporate products](https://www.accordfintech.com/corporate)
- NSE Terms of Use: users are "prohibited to conduct any systematic or automated data collection activities (including scraping, data mining, data extraction and data harvesting)", and unauthorised use may violate copyright and trademark law. NSE Clearing's terms have the same ban. — [NSE Terms of Use](https://www.nseindia.com/static/nse-terms-of-use); [NSE Clearing T&C](https://www.nseclearing.in/terms-conditions-0)
- Community discussion, low reliability, matches this: public display of NSE data requires buying from NSE or a registered vendor. — [Zerodha TradingQnA](https://tradingqna.com/t/need-api-for-nse-data/104916); [nsepy GitHub issue on legality](https://github.com/swapniljariwala/nsepy/issues/46)

### Inferences
- Corporate announcements, shareholding patterns and financial results are filed publicly with NSE and BSE. Taking them programmatically from exchange websites breaches the terms. A vendor feed (CMOTS, Accord) or NSE D&A's corporate data products is the compliant route.
- For an AI product, check that the licence covers derived or non-display use (LLM summarisation and embeddings). This is a non-display question NSE prices separately, per the Non_display document.
- From training knowledge, unverified: CMIE Prowess and Capitaline are mostly licensed to institutions and academia, with research-terminal pricing. Trendlyne and Tickertape do not publicly market redistribution APIs. Moneycontrol is part of Network18 and Reuters is part of LSEG, and both license news by enterprise agreement only.

### Gaps
- No price points found for CMOTS, Accord Datafeed, Capitaline, Prowess, the Trendlyne or Tickertape APIs, or news licences from PTI, Reuters, ET or Moneycontrol. All need direct quotes.
- No source found on whether CMOTS or Accord licences allow LLM processing or derived-data use.

## 3. Mutual fund data

### Takeaway
NAVs are free from AMFI's daily NAV file (AMFI retains the IP). The old format has been discontinued, so the parser needs checking. The big change is that in September 2025 AMFI directed MFCentral to stop sharing investor portfolio data with third-party platforms, which ended the one-click MF import that 100+ fintechs used. As of 2026, no public MFCentral developer API exists. Production MF holdings now come from CAS PDF parsing (CAMS/KFintech or NSDL/CDSL eCAS) or from Account Aggregator (CAMS and KFin RTA FIPs).

### Cited Findings
- The AMFI NAV file is at amfiindia.com/spages/NAVAll.txt, with a portal mirror showing current NAV dates (an April 2026 entry was seen). — [AMFI NAVAll.txt](https://www.amfiindia.com/spages/NAVAll.txt); [portal mirror](https://portal.amfiindia.com/spages/NAVAll.txt)
- AMFI's NAV download page says "NAV download in the old format has been discontinued" and asks users to move to the new format. — [AMFI NAV download](https://www.amfiindia.com/net-asset-value/nav-download)
- mftool is a Python library that pulls AMFI data with no external dependencies. — [mftool GitHub](https://github.com/NayakwadiS/mftool); [PyPI](https://pypi.org/project/mftool/1.6)
- Open-source projects note that AMFI data remains AMFI's intellectual property. — [get-navall GitHub](https://github.com/ukkit/get-navall)
- AMFI directed MF Central to suspend sharing investor portfolio data with third parties in September 2025, after distributor complaints about client poaching. More than 100 platforms were affected, including Groww and Kuvera. — [Business Today, 18 Sep 2025](https://www.businesstoday.in/personal-finance/news/story/why-amfi-blocked-fintechs-access-to-investor-data-a-look-at-the-concerns-and-impact-494695-2025-09-18); [CASParser blog (vendor, biased)](https://casparser.in/blog/mfcentral-shutdown-what-to-do/)
- A 2026 guide says MFCentral's new CEO (Feb 2026) has stressed API-first infrastructure, but no public API has launched. — [Monzy MFCentral guide 2026](https://blog.monzy.co/mutual-fund-guides/mfcentral-guide-cas-nominee-kyc)
- MF Central is run jointly by CAMS and KFintech, the two main RTAs. — [foliyo.ai guide](https://foliyo.ai/guides/mf-platforms/track-mfs-across-amcs/)

### Inferences
- Nivara can use AMFI NAVs for free for valuation. AMFI's IP terms on display should be read, but NAV display is industry standard.
- Scheme metadata (ratings, category, portfolio holdings, expense ratios, returns analytics) needs a licence from CMOTS or Accord (both list MF data) or from Value Research or Morningstar.

### Gaps
- mfapi.in: no search results confirmed its current availability or terms. It is an unofficial free API and should not be relied on for production.
- Value Research and Morningstar India data-licence pricing: not found.
- The exact new AMFI NAV file format and URL.

## 4. Holdings import routes

### Takeaway
There are four routes. (a) Broker APIs: mostly free or ₹499 a month per app for portfolio reads, but each is per-user OAuth with daily token expiry and covers one broker only. (b) smallcase Gateway: a multi-broker holdings import, including MF, by commercial quote. (c) Account Aggregator: covers demat (NSDL, CDSL), MF RTAs and NPS through regulated consent. Sahamati's standard per-fetch rate card takes effect 1 Dec 2026, and depositories return only 2 years of transactions per fetch. (d) CAS PDF upload with open-source casparser or the commercial CASParser API: cheapest and broadest, but manual and periodic.

### Cited Findings
Broker APIs
- Zerodha Kite Connect: the Personal tier is ₹0 and covers orders, GTT, alerts, portfolio, holdings and funds, but has no live or historical market data (launched March 2025). The Connect tier is ₹500 a month per API key and adds WebSocket and historical data (cut from ₹2,000). — [Zerodha support: Kite API charges](https://support.zerodha.com/category/trading-and-markets/kite-api/articles/what-are-the-charges-for-kite-apis); [kite.trade forum: fees ₹2000→₹500](https://kite.trade/forum/discussion/comment/49597); [Kite Personal APIs announcement](https://kite.trade/forum/discussion/comment/49196/); [marketcalls](https://www.marketcalls.in/fintech/zerodha-makes-trading-api-free-for-personal-use-bundles-historical-data-with-connect-api.html)
- Groww Trade API: ₹499 plus taxes a month (18% GST), with no usage fees. It covers holdings, positions, market data, orders and historical OHLC. Access tokens expire daily. Order placement needs a whitelisted static IP. Limits: orders 10/s and 250/min; live data 10/s and 300/min; non-trading 20/s and 500/min. — [Groww Trade API](https://groww.in/trade-api); [marketcalls Groww API 2026](https://www.marketcalls.in/fintech/groww-enters-the-algo-arena-with-powerful-trading-apis.html); [docs](https://groww.in/trade-api/docs)
- Angel One SmartAPI is free, including historical data and WebSocket. Fyers API is free, with an optional Prime tier at ₹499. Dhan's trading API is free and its Data API is ₹499 plus tax. Upstox sources conflict: one says ₹0, another says ₹10 per executed API order until 31 Mar 2026. All of these are third-party 2026 comparisons. — [knowyourbrokerage API pricing 2026](https://knowyourbrokerage.in/compare/trading-api-pricing); [cernoquant broker API charges 2026](https://cernoquant.com/blog/broker-api-charges-comparison); [stratzy](https://stratzy.in/blog/cost-comparison-algo-trading-apis-india/)

smallcase Gateway
- Gateway supports a "holdings import" transaction intent. The app creates a transactionId, the user logs into their broker, and holdings (with an optional MF flag) are returned through a fetch-holdings endpoint and webhooks. — [Create transaction: holdings import](https://developers.gateway.smallcase.com/reference/create-transaction-holdings-import); [Fetch holdings](https://developers.gateway.smallcase.com/reference/fetch-holdings); [Webhooks](https://developers.gateway.smallcase.com/docs/webhooks); [MF analytics API](https://developers.gateway.smallcase.com/docs/mf-analytics-api)
- Known issue: for some brokers, positions are not yet available, and quantity or average price can come back as 0 in Holdings Import v2. — [Holdings Import v2 known data discrepancy](https://developers.gateway.smallcase.com/page/holdings-import-v2-known-data-discrepancy)
- Pricing is licence-based and varies by user count. It is quote-only, per a third-party listing. — [fintegrationfs smallcase API](https://www.fintegrationfs.com/fintechapis/smallcase-api)

Account Aggregator
- Sahamati's standardised AA pricing (FIP fee + AA utility fee + Sahamati ecosystem fee, billed per successful fetch by the AA to the FIU) was deferred from 1 Nov to 1 Dec 2026. — [Elets BFSI](https://bfsi.eletsonline.com/sahamati-defers-account-aggregator-pricing-model-december-1-fiu-fip-fees/); [Whalesbook](https://www.whalesbook.com/news/English/bankingfinance/Sahamati-Pushes-Account-Aggregator-Fee-Model-to-December-1/6adf67494fc30694db4d383b)
- Business Standard (Oct 2026): the AA network "gets a rate card; tech middlemen cut out". It reports a split of ₹2.80 to the bank FIP and ₹0.40 to Sahamati, unit unclear. — [Business Standard](https://www.business-standard.com/industry/banking/account-aggregator-network-gets-a-rate-card-tech-middlemen-cut-out-126101201021_1.html)
- Depositories and MF RTAs return at most 2 years of transactions per fetch. One vendor (a competitor, so biased) estimates up to ₹96 plus GST per account for 20 years of investment history, that is, 10 fetches. — [casparser.in AA pricing 2026 (vendor)](https://casparser.in/blog/account-aggregator-pricing-2026/)
- Older Setu AA policy (around 2023): ₹0.01 to ₹25 per fetch. CRIF Connect: ₹5 to 25 per bank statement retrieval, excluding FIP charges. — [Setu AA pricing policy](https://setu-aa.com/pricing-policy); [CRIF Connect pricing](https://www.crifconnect.com/pricing)
- Sahamati directory (updated 31 Oct 2026): NSDL and CDSL are live as FIPs, KFin RTA is live as FIP, KFin NPS and Protean NPS-CRA are live as FIPs. A June 2026 Sahamati timeline lists CAMS RTA live as FIP and FIU, and CAMS NPS live as FIP. — [Sahamati FIPs & FIUs](https://sahamati.org.in/fip-fiu-in-account-aggregators-ecosystem/); [Sahamati FI types by non-bank FIPs](https://sahamati.org.in/fi-types-activated-by-non-banking-fips-on-aa/); [Sahamati AA timeline](https://sahamati.org.in/account-aggregator-timeline/); [NSDL FIP](https://nsdl.co.in/value/Financial_Information_Provider.php)
- A March 2026 builder's guide says equities, MF units, ETFs, AIFs and REITs are live through CDSL and NSDL on 13 AAs, with demat history capped at 2 years. It counts 179 FIPs and 955 FIUs. — [ecorpit AA builder's guide 2026](https://ecorpit.com/account-aggregator-integration-fintech-builders-2026/); [casparser state of AA 2026 (vendor)](https://casparser.in/blog/state-of-account-aggregator-2026/)
- AA setup as an FIU is described as slow and costly, around 5 to 10 months. This is vendor-sourced. — [CASParser comparison (vendor)](https://casparser.in/comparison/)

CAS parsing
- casparser (open source, codereverser) parses CAMS/KFintech CAS PDFs locally. A non-empty parse_warnings means at least one scheme failed to reconcile with the printed running unit balance. It rejects re-printed PDFs whose watermark or metadata has been flattened. At last check it had about 85 stars, 4 open and 28 closed issues. Snyk shows no known direct vulnerabilities. — [casparser GitHub](https://github.com/codereverser/casparser); [kandi](https://kandi.openweaver.com/python/codereverser/casparser); [Snyk](https://security.snyk.io/package/pip/casparser)
- The commercial CASParser API (SDKs in Python, Node, Go and PHP) covers NSDL, CDSL, CAMS and KFintech CAS. It claims 97% parse accuracy and 99.9% uptime, both self-reported. The SDK is version 0.x and its API may change. — [CASParser python SDK](https://github.com/CASParser/cas-parser-python); [CASParser features](https://casparser.in/features/)

### Inferences
- For Nivara's existing Groww integration: ₹499 a month buys one developer subscription. Each end user would need their own Groww API subscription and token, so it is not a scalable consumer holdings route. Kite Personal (free) has the same per-user constraint. The scalable broker route is a registered multi-user app (Kite Connect at ₹500 a month per app key, or Upstox, Angel or Fyers OAuth apps) or smallcase Gateway.
- The AA route needs Nivara itself to be a regulated entity (an FIU under a sector regulator such as a SEBI-registered RIA or RA, or a licensed partner). This is an onboarding requirement to check with the regulatory researcher.
- Recommended mix for broad coverage: CAS upload (all MF + demat, free, open-source) → AA (refreshable, consented) → broker OAuth (live for active traders).

### Gaps
- No current per-fetch rate cards found for Setu, Finvu, OneMoney, Anumati or Saafe under the 1 Dec 2026 model. The official Sahamati circular was not located.
- EPF (EPFO) as an FIP: no source found that it is live on AA.
- Motilal Oswal, ICICI Breeze and Upstox (official) API pricing and terms: not confirmed in this research.
- smallcase Gateway's actual fees.

## 5. How competitors source holdings and market data

### Takeaway
Public evidence is mostly secondhand. INDmoney reportedly combines CAS import, AA bank linkage and EPF via UAN. Kuvera relied on CAS and MF Central and was affected by the Sept 2025 MFCentral cut-off. Tickertape uses broker links and broker statements. smallcase Gateway is a working multi-broker aggregator for equities and MF holdings, but coverage varies by broker.

### Cited Findings
- INDmoney: third-party reviews describe CAS import, AA for bank data and EPF via UAN. One says external MF holdings came via MF Central and that CAS-refresh data is not real-time. — [foliyo.ai INDmoney review](https://foliyo.ai/guides/mf-platforms/indmoney-review/); [GetBelong 2026](https://getbelong.com/blog/portfolio-tracker-apps-in-india/)
- Kuvera: MF data from CAMS/KFintech CAS, plus broker import and UAN link. — [allinvestview 2026](https://www.allinvestview.com/best-portfolio-tracker-india/); [GetBelong](https://getbelong.com/blog/portfolio-tracker-apps-in-india/)
- Groww and Kuvera were among 100+ platforms that lost MF Central portfolio access in Sept 2025. — [Business Today](https://www.businesstoday.in/personal-finance/news/story/why-amfi-blocked-fintechs-access-to-investor-data-a-look-at-the-concerns-and-impact-494695-2025-09-18)
- Tickertape: portfolio links to brokers such as Zerodha and Groww, or uploads a broker statement. It reportedly does not support FDs, EPF, NPS or US stocks. — [invsify](https://invsify.com/blog/portfolio-tracking-app-india); [futurecaps](https://futurecaps.com/portfolio-tracker-app/)
- Review sources conflict on INDmoney (email reading versus broker sync only). — [invsify online investment tracker](https://invsify.com/blog/online-investment-tracker)

### Inferences
- smallcase Gateway is viable for a fast multi-broker equity import without building N broker integrations. Expect a commercial agreement and per-broker data quirks, such as zero quantity or price for some brokers.
- From training knowledge, unverified: Tickertape (owned by smallcase) likely uses smallcase Gateway internally, and its market data comes from licensed vendors. I found no public source.

### Gaps
- No official disclosures from INDmoney, Kuvera or Tickertape about which market-data vendors they use.

## 6. Recommended phased architecture and approximate monthly cost

### Takeaway
Phase 0/1 (beta, a few thousand users): keep everything licensed but low-cost. Use AMFI NAVs (free), a vendor's EOD or 15-min-delayed sublicence plus a basic fundamentals and corporate-actions basket (CMOTS or Accord, quote-based), CAS upload through open-source casparser, and per-user broker OAuth (Kite Connect app ₹500 a month, Upstox, Angel, Fyers free). Phase 2: add an AA partner (Setu or Finvu) for refreshable demat and MF, and smallcase Gateway if broker breadth matters. Phase 3 (scale): a direct NSE D&A licence for real-time display, a licensed news feed, and MF research data (Value Research or Morningstar).

### Cited Findings
- Kite Connect costs ₹500 a month per app and Groww ₹499 a month, Angel and Fyers are free, and the Dhan Data API is ₹499. — see the sources in Section 4.
- NSE 15-min delayed CM is ₹90k a year, and real-time terminal or mobile licences ran ₹11.5 to 24 lakh or more a year in 2025. — see the sources in Section 1.
- Sahamati AA per-fetch fees start on 1 Dec 2026, with depository history at 2 years per fetch. — see the sources in Section 4.
- CMOTS has 12-month basket subscriptions, and Ace Equity Nxt starts at ₹1.25 lakh a year (research use). — see the sources in Section 2.

### Inferences (indicative and unverified; get quotes)
- Beta monthly cost estimate: broker API apps ₹500 to 1,500; a delayed or EOD market data plus fundamentals vendor basket at very roughly ₹15,000 to 50,000 a month (based on the NSE ₹90k-a-year delayed floor plus the vendor margin and fundamentals basket; no CMOTS or Accord price was found); CAS parsing ₹0 self-hosted; AMFI NAV ₹0. Total of roughly ₹20k to 60k a month plus GST.
- AA at beta: assuming about ₹10 to 30 per account-fetch (based on old Setu and CRIF ranges and the ₹96-for-10-fetches vendor estimate), 3,000 users × 2 accounts × 1 refresh a month comes to roughly ₹60k to 1.8 lakh a month. This is why AA should be optional or on-demand refresh, not a daily sync.
- Scale (100k+ users): direct NSE real-time display at ₹25 to 30 lakh or more a year in fixed fees plus per-user fees (about ₹875 per user per month in one secondary source, which would be prohibitive for free users, so a delayed default with real-time for paying users makes sense), plus news licences, plus MF research data. Total is likely ₹5 to 15 lakh or more a month. This is unverified.
- Architecture: keep the existing provider interface. Add a `LicensedMarketDataProvider` (vendor), `NavProvider` (AMFI), `FundamentalsProvider` (CMOTS or Accord), and `HoldingsSource` adapters (CAS, broker OAuth, smallcase, AA). Tag every record with source, licence and timestamp, and block yfinance from production display paths.

### Gaps
- No vendor quotes were obtained. All beta and scale cost totals are estimates built from partial tariffs.
- Regulatory prerequisites for becoming an FIU (which regulator, and whether Nivara's SEBI status qualifies) are outside this scope.
