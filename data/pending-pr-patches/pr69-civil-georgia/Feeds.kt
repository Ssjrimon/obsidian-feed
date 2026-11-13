<cursor_untrusted_data_1337 source="CallDynamicTool">

package com.novaboy.obsidian.core

/**
 * Open RSS feeds, no accounts or API keys. A feed that is down or has moved
 * costs nothing but its own headlines; the briefing is built from whichever
 * ones answer. Add or remove entries freely.
 */
object Feeds {
    val ALL: List<FeedSource> = listOf(
        // World
        FeedSource("bbc-world", "BBC", "https://feeds.bbci.co.uk/news/world/rss.xml"),
        FeedSource("bbc-me", "BBC", "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml", Region.MIDEAST),
        FeedSource("bbc-eu", "BBC", "https://feeds.bbci.co.uk/news/world/europe/rss.xml", Region.EUROPE),
        FeedSource("bbc-asia", "BBC", "https://feeds.bbci.co.uk/news/world/asia/rss.xml", Region.INDOPAC),
        FeedSource("bbc-africa", "BBC", "https://feeds.bbci.co.uk/news/world/africa/rss.xml", Region.AFRICA),
        FeedSource("aljazeera", "AL JAZEERA", "https://www.aljazeera.com/xml/rss/all.xml"),
        FeedSource("guardian", "GUARDIAN", "https://www.theguardian.com/world/rss"),
        FeedSource("dw", "DW", "https://rss.dw.com/rdf/rss-en-all"),
        // United States
        FeedSource("bbc-us", "BBC", "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", Region.HOMELAND),
        FeedSource("npr", "NPR", "https://feeds.npr.org/1001/rss.xml", Region.HOMELAND),
        // Reuters withdrew its public RSS in 2020. This is Google News filtered to
        // reuters.com: headlines only, and it depends on Google continuing to serve it.
        FeedSource(
            "reuters", "REUTERS",
            "https://news.google.com/rss/search?q=site:reuters.com+when:1d&hl=en-US&gl=US&ceid=US:en",
            headlinesOnly = true
        ),
        // Middle East. Regional outlets and an official advisory source.
        FeedSource("toi", "TIMES OF ISRAEL", "https://www.timesofisrael.com/feed/", Region.ISRAEL),
        FeedSource("jpost", "JERUSALEM POST", "https://www.jpost.com/rss/rssfeedsheadlines.aspx", Region.ISRAEL),
        FeedSource("mee", "MIDDLE EAST EYE", "https://www.middleeasteye.net/rss", Region.MIDEAST),
        FeedSource("almonitor", "AL-MONITOR", "https://www.al-monitor.com/rss", Region.MIDEAST),
        FeedSource("travel", "STATE DEPT", "https://travel.state.gov/_res/rss/TAsTWs.xml", Region.MIDEAST, Category.POLITICAL, primary = true),
        // Google News searches stand in for regional outlets with no RSS. Always the US English
        // edition, so the requests look the same from anywhere.
        FeedSource(
            "gn-levant", "GOOGLE NEWS",
            "https://news.google.com/rss/search?q=Syria+OR+Lebanon+OR+Iraq+when:2d&hl=en-US&gl=US&ceid=US:en",
            Region.MIDEAST, headlinesOnly = true
        ),
        FeedSource(
            "gn-region", "GOOGLE NEWS",
            "https://news.google.com/rss/search?q=Houthi+OR+Hezbollah+OR+Iraq+militia+OR+Syria+drone+when:1d&hl=en&gl=US&ceid=US:en",
            Region.MIDEAST, headlinesOnly = true
        ),
        // Defense. The Stars and Stripes address was fetched and parsed: it answers with a dated RSS feed.
        FeedSource("stripes", "STARS AND STRIPES", "https://subscribe.stripes.com/rss/top-news.xml", null, Category.KINETIC),
        FeedSource("defensenews", "DEFENSE NEWS", "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml", null, Category.KINETIC),
        FeedSource("twz", "THE WAR ZONE", "https://www.twz.com/feed", null, Category.KINETIC),
        FeedSource("breakingdefense", "BREAKING DEFENSE", "https://breakingdefense.com/feed/", null, Category.KINETIC),
        // Tech and cyber
        FeedSource("ars", "ARS TECHNICA", "https://feeds.arstechnica.com/arstechnica/index", null, Category.TECH),
        FeedSource("mit", "MIT TECH REVIEW", "https://www.technologyreview.com/feed/", null, Category.TECH),
        FeedSource("bbc-tech", "BBC", "https://feeds.bbci.co.uk/news/technology/rss.xml", null, Category.TECH),
        FeedSource("nasa", "NASA", "https://www.nasa.gov/feed/", null, Category.TECH),
        FeedSource("bleeping", "BLEEPINGCOMPUTER", "https://www.bleepingcomputer.com/feed/", null, Category.CYBER),
        FeedSource("cyberdive", "CYBERSECURITY DIVE", "https://www.cybersecuritydive.com/feeds/news/", null, Category.CYBER),
        // Primary sources: governments and commands publishing their own advisories and statements.
        // Carried as attributed claims (see FeedSource.primary), never as independent confirmation.
        FeedSource("cisa", "CISA", "https://www.cisa.gov/cybersecurity-advisories/all.xml", null, Category.CYBER, primary = true),
        // The catalog of vulnerabilities known to be exploited: structured data, read by its own parser. Same
        // publisher as the line above, so the two count as one source when outlets are tallied.
        FeedSource(
            "cisa-kev", "CISA", "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            null, Category.CYBER, primary = true, format = FeedFormat.KEV
        ),
        FeedSource(
            "centcom", "CENTCOM",
            "https://www.centcom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=808&max=10",
            Region.MIDEAST, Category.KINETIC, primary = true
        ),
        FeedSource(
            "dow", "DEPT OF WAR",
            "https://www.war.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=10",
            null, Category.KINETIC, primary = true
        ),
        // Theatre and maritime reporting
        FeedSource("kyivind", "KYIV INDEPENDENT", "https://kyivindependent.com/news-archive/rss/", Region.UKRAINE),
        FeedSource("gcaptain", "GCAPTAIN", "https://gcaptain.com/feed/"),
        FeedSource("france24", "FRANCE 24", "https://www.france24.com/en/rss"),
        FeedSource("pbs", "PBS NEWSHOUR", "https://www.pbs.org/newshour/feeds/rss/world"),
        FeedSource("axios", "AXIOS", "https://api.axios.com/feed/"),
        // Regions the list above covers thinly. Each address was fetched and parsed by this app's own
        // parser, and each carries dated items inside the 48-hour window.
        // Pacific and Southeast Asia
        FeedSource("rnz-pacific", "RNZ", "https://www.rnz.co.nz/rss/pacific.xml", Region.INDOPAC),
        FeedSource("postcourier", "POST-COURIER", "https://postcourier.com.pg/feed/", Region.INDOPAC),
        FeedSource("islandsbusiness", "ISLANDS BUSINESS", "https://islandsbusiness.com/feed/", Region.INDOPAC),
        FeedSource("irrawaddy", "IRRAWADDY", "https://www.irrawaddy.com/feed", Region.INDOPAC),
        FeedSource("bangkokpost", "BANGKOK POST", "https://www.bangkokpost.com/rss/data/most-recent.xml", Region.INDOPAC),
        FeedSource("straitstimes", "STRAITS TIMES", "https://www.straitstimes.com/news/singapore/rss.xml", Region.INDOPAC),
        // South Asia
        FeedSource("thehindu", "THE HINDU", "https://www.thehindu.com/feeder/default.rss", Region.SOUTHASIA),
        // Africa
        FeedSource("nation", "NATION", "https://nation.africa/kenya/rss.xml", Region.AFRICA),
        FeedSource("premiumtimes", "PREMIUM TIMES", "https://www.premiumtimesng.com/feed/", Region.AFRICA),
        FeedSource("punch", "PUNCH", "https://punchng.com/feed/", Region.AFRICA),
        // Latin America
        FeedSource("mercopress", "MERCOPRESS", "https://en.mercopress.com/rss/", Region.LATAM),
        // Caucasus
        FeedSource("civilgeorgia", "CIVIL GEORGIA", "https://civil.ge/feed", Region.CAUCASUS),
        // Measurements and alert series. Each address was fetched with no key. They can confirm a
        // news report about the same place and time. None of them carries a position of the wearer.
        // Category is set so a quiet day here is not read as "this area was not checked".
        FeedSource(
            "usgs-significant", "USGS",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson",
            null, Category.GENERAL, format = FeedFormat.USGS, hardData = true, hardKind = HardKind.QUAKE
        ),
        FeedSource(
            "usgs-m45", "USGS",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
            null, Category.GENERAL, format = FeedFormat.USGS, hardData = true, hardKind = HardKind.QUAKE
        ),
        FeedSource(
            "gdacs", "GDACS",
            "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=EQ;TC;FL;VO;WF;DR&alertlevel=Orange;Red",
            null, Category.GENERAL, format = FeedFormat.GDACS, hardData = true
        ),
        FeedSource(
            "who-don", "WHO",
            "https://www.who.int/api/news/diseaseoutbreaknews?\$orderby=PublicationDateAndTime%20desc&\$top=8&\$select=Title,OverrideTitle,UseOverrideTitle,PublicationDateAndTime,UrlName,Summary,DonId",
            null, Category.GENERAL, format = FeedFormat.WHO, hardData = true, hardKind = HardKind.OUTBREAK
        ),
        FeedSource(
            "eonet-storms", "NASA EONET",
            "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=8&category=severeStorms",
            null, Category.GENERAL, format = FeedFormat.EONET, hardData = true, hardKind = HardKind.STORM
        ),
        FeedSource(
            "eonet-volcanoes", "NASA EONET",
            "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=8&category=volcanoes",
            null, Category.GENERAL, format = FeedFormat.EONET, hardData = true, hardKind = HardKind.VOLCANO
        ),
        FeedSource(
            "fema", "FEMA",
            "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?\$top=80&\$orderby=declarationDate%20desc&\$select=disasterNumber,declarationTitle,state,declarationDate,incidentType",
            Region.HOMELAND, Category.GENERAL, format = FeedFormat.FEMA, hardData = true
        ),
        FeedSource(
            "noaa-tsunami", "NOAA",
            "https://www.tsunami.gov/events/xml/PHEBAtom.xml",
            null, Category.GENERAL, hardData = true, hardKind = HardKind.TSUNAMI
        )
    )

    /** Publishers whose reports are official statements (attributed claims). */
    val PRIMARY_PUBLISHERS: Set<String> = ALL.filter { it.primary }.map { it.name }.toSet()
}


</cursor_untrusted_data_1337>