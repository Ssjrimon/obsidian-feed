<cursor_untrusted_data_1337 source="CallDynamicTool">

package com.novaboy.obsidian.core

/**
 * How much weight an outlet's own record carries. A tier is a judgement about the publisher, never
 * about a particular report, and it is shown in Settings rather than hidden inside the scoring.
 */
enum class Tier(val label: String, val countsAsIndependent: Boolean) {
    /** Wire services and major broadcasters with a long reporting record. */
    ESTABLISHED("established", true),
    /** Reputable outlets covering one country or region. */
    REGIONAL("regional", true),
    /** Trade and subject specialists: defence, maritime, cyber, science. */
    SPECIALIST("specialist", true),
    /** Owned or funded by a state and editorially answerable to it: a claim, never corroboration. */
    STATE_AFFILIATED("state-affiliated", false),
    /** Campaigning or opinion-led: carried, but never counted as corroboration. */
    PARTISAN("partisan", false),
    /** A government or command publishing its own statements. */
    OFFICIAL("official", false),
    /** Republishes other outlets, so the real publisher is unknown. */
    AGGREGATOR("aggregator", false),
    /** Not rated yet. Counted, but shown as unrated so it is obvious. */
    UNKNOWN("unrated", true),

    /**
     * A public measurement or alert series (quakes, disaster alerts, outbreak notices). Counted as
     * its own source. It is not a newsroom, and it is not a government describing its own actions.
     */
    DATA_SET("data set", true)
}

/**
 * One publisher, with the group it belongs to for independence. Two outlets in the same group are
 * one source however many of them print the story: a wire and its subscribers, or two arms of one
 * government.
 */
data class Outlet(
    val name: String,
    val tier: Tier,
    /** Stable id of the independence group. */
    val group: String,
    /** How that group reads on screen. */
    val groupLabel: String,
    /** Anything the reader should know about who funds or runs it. */
    val note: String? = null
)

/** What a story's outlets add up to: how many bodies really stand behind it. */
data class Sourcing(
    /** Every publisher that printed it. */
    val outlets: List<Outlet>,
    /** Independence groups among the outlets that count: the honest source count. */
    val independentGroups: List<String>,
    /** Group labels, for display. */
    val independentLabels: List<String>,
    /** Wire services whose copy replaced a publisher's own group. */
    val viaWire: List<String> = emptyList()
) {
    val outletCount: Int get() = outlets.size
    val sourceCount: Int get() = independentGroups.size
    /** True when several outlets collapse to fewer real sources, so the gap is worth showing. */
    val collapses: Boolean get() = outletCount > sourceCount
    val hasOfficial: Boolean get() = outlets.any { it.tier == Tier.OFFICIAL }
    val hasStateAffiliated: Boolean get() = outlets.any { it.tier == Tier.STATE_AFFILIATED }
    /** Every publisher on the story is a data set, so the story is a measurement rather than news. */
    val dataSetOnly: Boolean get() = outlets.isNotEmpty() && outlets.all { it.tier == Tier.DATA_SET }

    /** Said when a publisher is carrying a wire rather than its own reporting. */
    fun viaWireNote(): String? {
        if (viaWire.isEmpty()) return null
        return "Carries ${viaWire.joinToString(" and ")}. Outlets running the same wire count as one source."
    }

    /**
     * How the sourcing reads on a report: the real source count, and the outlet count beside it
     * when several outlets collapse into fewer sources.
     */
    fun summary(): String {
        val sources = if (sourceCount == 1) "1 SOURCE" else "$sourceCount SOURCES"
        return if (collapses) "$sources · $outletCount OUTLETS" else sources
    }
}

/**
 * The source registry: who each publisher is, how far its record carries, and who it is
 * independent of. Hand-written and meant to be read: nothing here is inferred from the feeds.
 */
object Outlets {
    private fun o(name: String, tier: Tier, group: String, groupLabel: String, note: String? = null) =
        Outlet(name, tier, group, groupLabel, note)

    val ALL: List<Outlet> = listOf(
        // Established: wire services and major broadcasters.
        o("REUTERS", Tier.ESTABLISHED, "reuters", "Reuters"),
        o("BBC", Tier.ESTABLISHED, "bbc", "BBC"),
        o("GUARDIAN", Tier.ESTABLISHED, "guardian", "Guardian"),
        o("NPR", Tier.ESTABLISHED, "npr", "NPR"),
        o("PBS NEWSHOUR", Tier.ESTABLISHED, "pbs", "PBS"),
        o("AXIOS", Tier.ESTABLISHED, "axios", "Axios"),
        o("DW", Tier.ESTABLISHED, "dw", "Deutsche Welle", "German public broadcaster, editorially independent by statute"),
        // Regional: one country or region, with their own standing.
        o("AL JAZEERA", Tier.REGIONAL, "aljazeera", "Al Jazeera", "Qatari state-funded; separate newsroom"),
        o("FRANCE 24", Tier.REGIONAL, "france24", "France 24", "French state-funded international broadcaster"),
        o("TIMES OF ISRAEL", Tier.REGIONAL, "toi", "Times of Israel"),
        o("JERUSALEM POST", Tier.REGIONAL, "jpost", "Jerusalem Post"),
        o("MIDDLE EAST EYE", Tier.REGIONAL, "mee", "Middle East Eye"),
        o("AL-MONITOR", Tier.REGIONAL, "almonitor", "Al-Monitor"),
        o("KYIV INDEPENDENT", Tier.REGIONAL, "kyivindependent", "Kyiv Independent"),
        o("RNZ", Tier.REGIONAL, "rnz", "RNZ", "New Zealand public broadcaster; its Pacific desk"),
        o("POST-COURIER", Tier.REGIONAL, "postcourier", "Post-Courier", "Papua New Guinea. Often runs the PACNEWS regional wire, so an item here may also appear in other Pacific papers"),
        o("ISLANDS BUSINESS", Tier.REGIONAL, "islandsbusiness", "Islands Business", "Pacific regional magazine. Ownership not checked"),
        o("IRRAWADDY", Tier.REGIONAL, "irrawaddy", "Irrawaddy", "Myanmar outlet reporting largely from exile. Ownership not checked"),
        o("BANGKOK POST", Tier.REGIONAL, "bangkokpost", "Bangkok Post"),
        o("THE HINDU", Tier.REGIONAL, "thehindu", "The Hindu"),
        o("NATION", Tier.REGIONAL, "nmg", "Nation Media Group", "Kenya. Ownership not checked"),
        o("PREMIUM TIMES", Tier.REGIONAL, "premiumtimes", "Premium Times", "Nigeria. Ownership not checked"),
        o("PUNCH", Tier.REGIONAL, "punch", "Punch", "Nigeria. Ownership not checked"),
        o("CIVIL GEORGIA", Tier.REGIONAL, "civilgeorgia", "Civil Georgia", "Independent English news, Georgia / South Caucasus. Ownership not checked"),
        // Not rated: ownership could not be established, so it counts but is shown as unrated.
        o("MERCOPRESS", Tier.UNKNOWN, "mercopress", "MercoPress", "Ownership could not be established"),
        // Government-funded and described as government-aligned by one monitor. The classification is
        // contested, so it is treated as not independent: it can be read but never corroborates alone.
        o("STRAITS TIMES", Tier.STATE_AFFILIATED, "sph", "SPH Media", "Receives government funding; ministerial approval is needed for its management shares"),
        // Specialists: a subject each, with real expertise in it.
        o("STARS AND STRIPES", Tier.SPECIALIST, "stripes", "Stars and Stripes", "US Defense Department funded; editorially independent by law"),
        o("DEFENSE NEWS", Tier.SPECIALIST, "defensenews", "Defense News"),
        o("THE WAR ZONE", Tier.SPECIALIST, "twz", "The War Zone"),
        o("BREAKING DEFENSE", Tier.SPECIALIST, "breakingdefense", "Breaking Defense"),
        o("GCAPTAIN", Tier.SPECIALIST, "gcaptain", "gCaptain"),
        o("ARS TECHNICA", Tier.SPECIALIST, "ars", "Ars Technica"),
        o("MIT TECH REVIEW", Tier.SPECIALIST, "mit", "MIT Technology Review"),
        o("BLEEPINGCOMPUTER", Tier.SPECIALIST, "bleeping", "BleepingComputer"),
        o("CYBERSECURITY DIVE", Tier.SPECIALIST, "cyberdive", "Cybersecurity Dive"),
        // Official: one government, so one group however many of its arms publish.
        o("STATE DEPT", Tier.OFFICIAL, "us-gov", "US government"),
        o("CENTCOM", Tier.OFFICIAL, "us-gov", "US government"),
        o("DEPT OF WAR", Tier.OFFICIAL, "us-gov", "US government"),
        o("CISA", Tier.OFFICIAL, "us-gov", "US government"),
        o("NASA", Tier.OFFICIAL, "us-gov", "US government"),
        // Aggregator: the headline is someone else's, and the feed does not say whose.
        o("GOOGLE NEWS", Tier.AGGREGATOR, "googlenews", "Google News", "Republishes other outlets; the real publisher is not given"),
        // Data sets: a measurement or an alert series. Each stands alone, and none of them is news.
        o("USGS", Tier.DATA_SET, "usgs", "USGS", "US Geological Survey earthquake measurements. A quake is a quake, not a claim about its cause"),
        o("GDACS", Tier.DATA_SET, "gdacs", "GDACS", "UN and European Commission disaster alerts. Orange and red only; public-domain data"),
        o("WHO", Tier.DATA_SET, "who", "WHO", "World Health Organization Disease Outbreak News. Titles and a short summary only"),
        o("NASA EONET", Tier.DATA_SET, "eonet", "NASA EONET", "NASA's catalogue of open storms and eruptions. A track is not a cause"),
        o("FEMA", Tier.DATA_SET, "fema", "FEMA", "US disaster declarations. Public domain"),
        o("NOAA", Tier.DATA_SET, "noaa", "NOAA", "Pacific Tsunami Warning Center statements")
    )

    private val byName: Map<String, Outlet> = ALL.associateBy { it.name }

    init {
        // Every publisher the app fetches must be rated here, or its reports would read "unrated".
        val missing = Feeds.ALL.map { it.name }.distinct().filter { it !in byName }
        require(missing.isEmpty()) { "outlets missing from the registry: $missing" }
        val clashes = ALL.groupBy { it.group }.filterValues { g -> g.map { it.groupLabel }.distinct().size > 1 }
        require(clashes.isEmpty()) { "one group with two labels: ${clashes.keys}" }
    }

    /** The registry entry for [name], or an unrated outlet standing alone in its own group. */
    fun of(name: String): Outlet =
        byName[name] ?: Outlet(name, Tier.UNKNOWN, "?" + name.lowercase(), name)

    /** Grouped by independence group, for the Settings table. */
    fun byGroup(): List<Pair<String, List<Outlet>>> =
        ALL.groupBy { it.groupLabel }.toList().sortedBy { it.first.lowercase() }

    /**
     * What [outletNames] really add up to. Order is kept, duplicates dropped. [wireCredit] maps a
     * publisher to the wire group its copy belongs to, when the text credits AP, Reuters or AFP:
     * those copies share that wire's group instead of counting as their own newsroom.
     */
    fun sourcing(outletNames: List<String>, wireCredit: Map<String, String> = emptyMap()): Sourcing {
        val outlets = outletNames.distinct().map(::of)
        val groups = mutableListOf<String>()
        val labels = mutableListOf<String>()
        val via = mutableListOf<String>()
        for (outlet in outlets) {
            val credited = wireCredit[outlet.name]
            if (credited != null) {
                val label = WireCredits.labelOf(credited)
                if (credited !in groups) {
                    groups += credited
                    labels += label
                }
                if (label !in via) via += label
                continue
            }
            if (!outlet.tier.countsAsIndependent) continue
            if (outlet.group !in groups) {
                groups += outlet.group
                labels += outlet.groupLabel
            }
        }
        return Sourcing(outlets, groups, labels, via)
    }

    fun sourcing(story: Story): Sourcing = sourcing(story.sources, story.wireCredit)
}


</cursor_untrusted_data_1337>