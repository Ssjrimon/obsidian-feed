# Offline gazetteer: name/alias -> (iso2, lat, lon). Coordinates are country/area centroids.
COUNTRIES = {
 "UA":("Ukraine",["ukraine","ukrainian","kyiv","kiev","kharkiv","odesa","odessa","zaporizhzhia","donetsk","luhansk","kherson","dnipro","lviv","crimea"],48.4,31.2),
 "RU":("Russia",["russia","russian","moscow","kremlin","putin","st petersburg","belgorod","kursk"],55.75,37.6),
 "IL":("Israel",["israel","israeli","tel aviv","jerusalem","idf","netanyahu"],31.5,34.9),
 "PS":("Palestine",["gaza","palestinian","hamas","rafah","khan younis"],31.4,34.4),
 "LB":("Lebanon",["lebanon","lebanese","beirut","hezbollah"],33.9,35.5),
 "SY":("Syria",["syria","syrian","damascus","aleppo","idlib"],34.8,38.9),
 "IQ":("Iraq",["iraq","iraqi","baghdad","mosul","erbil","basra"],33.2,43.7),
 "IR":("Iran",["iran","iranian","tehran","irgc","khamenei"],32.4,53.7),
 "YE":("Yemen",["yemen","yemeni","houthi","houthis","sanaa","aden"],15.5,48.5),
 "SA":("Saudi Arabia",["saudi","riyadh","jeddah"],23.9,45.1),
 "AE":("United Arab Emirates",["uae","emirates","emirati","abu dhabi","dubai"],24.3,54.4),
 "QA":("Qatar",["qatar","qatari","doha"],25.3,51.2),
 "KW":("Kuwait",["kuwait"],29.3,47.5),
 "BH":("Bahrain",["bahrain"],26.0,50.5),
 "OM":("Oman",["oman","omani","muscat"],21.5,55.9),
 "JO":("Jordan",["jordan","amman"],31.2,36.5),
 "EG":("Egypt",["egypt","egyptian","cairo","sinai"],26.8,30.8),
 "TR":("Turkey",["turkey","turkish","turkiye","türkiye","ankara","istanbul","erdogan"],39.0,35.2),
 "PK":("Pakistan",["pakistan","pakistani","islamabad","karachi","lahore","balochistan"],30.4,69.3),
 "AF":("Afghanistan",["afghanistan","afghan","kabul","taliban"],33.9,67.7),
 "IN":("India",["india","indian","new delhi","delhi","mumbai","kashmir","modi"],20.6,79.0),
 "BD":("Bangladesh",["bangladesh","dhaka"],23.7,90.4),
 "LK":("Sri Lanka",["sri lanka","colombo"],7.9,80.8),
 "NP":("Nepal",["nepal","kathmandu"],28.4,84.1),
 "CN":("China",["china","chinese","beijing","shanghai","xi jinping","pla "],35.9,104.2),
 "TW":("Taiwan",["taiwan","taiwanese","taipei"],23.7,121.0),
 "JP":("Japan",["japan","japanese","tokyo","okinawa"],36.2,138.3),
 "KR":("South Korea",["south korea","south korean","s. korea","s.korea","seoul"],35.9,127.8),
 "KP":("North Korea",["north korea","north korean","n. korea","n.korea","dprk","pyongyang","kim jong"],40.3,127.5),
 "PH":("Philippines",["philippines","philippine","filipino","manila"],12.9,121.8),
 "MM":("Myanmar",["myanmar","burma","yangon","naypyidaw"],21.9,95.9),
 "TH":("Thailand",["thailand","thai","bangkok"],15.9,100.9),
 "KH":("Cambodia",["cambodia","phnom penh"],12.6,104.9),
 "VN":("Vietnam",["vietnam","vietnamese","hanoi"],14.1,108.3),
 "ID":("Indonesia",["indonesia","indonesian","jakarta"],-0.8,113.9),
 "MY":("Malaysia",["malaysia","kuala lumpur"],4.2,102.0),
 "AU":("Australia",["australia","australian","canberra","sydney"],-25.3,133.8),
 "GE":("Georgia",["tbilisi","georgian government"],42.3,43.4),
 "AM":("Armenia",["armenia","armenian","yerevan"],40.1,45.0),
 "AZ":("Azerbaijan",["azerbaijan","baku"],40.1,47.6),
 "PL":("Poland",["poland","polish","warsaw"],51.9,19.1),
 "BY":("Belarus",["belarus","belarusian","minsk","lukashenko"],53.7,28.0),
 "MD":("Moldova",["moldova","chisinau","transnistria"],47.4,28.4),
 "RO":("Romania",["romania","romanian","bucharest"],45.9,25.0),
 "EE":("Estonia",["estonia","tallinn"],58.6,25.0),
 "LV":("Latvia",["latvia","riga"],56.9,24.6),
 "LT":("Lithuania",["lithuania","vilnius"],55.2,23.9),
 "FI":("Finland",["finland","finnish","helsinki"],61.9,25.7),
 "GB":("United Kingdom",["britain","british","london","starmer"," uk "],51.5,-0.1),
 "FR":("France",["france","french","paris","macron"],46.2,2.2),
 "DE":("Germany",["germany","german","berlin"],51.2,10.5),
 "IT":("Italy",["italy","italian","rome"],41.9,12.6),
 "ES":("Spain",["spain","spanish","madrid"],40.5,-3.7),
 "RS":("Serbia",["serbia","belgrade"],44.0,21.0),
 "XK":("Kosovo",["kosovo","pristina"],42.6,20.9),
 "HU":("Hungary",["hungary","budapest","orban"],47.2,19.5),
 "GR":("Greece",["greece","greek","athens"],39.1,21.8),
 "BG":("Bulgaria",["bulgaria","sofia"],42.7,25.5),
 "LY":("Libya",["libya","libyan","tripoli","benghazi"],26.3,17.2),
 "SD":("Sudan",["sudan","sudanese","khartoum","darfur","rsf ","el fasher"],12.9,30.2),
 "SS":("South Sudan",["south sudan","juba"],6.9,31.3),
 "SO":("Somalia",["somalia","somali","mogadishu","al-shabaab","al shabaab"],5.2,46.2),
 "ET":("Ethiopia",["ethiopia","ethiopian","addis ababa","tigray","amhara"],9.1,40.5),
 "ER":("Eritrea",["eritrea"],15.2,39.8),
 "KE":("Kenya",["kenya","kenyan","nairobi"],-0.0,37.9),
 "ML":("Mali",["mali","malian","bamako"],17.6,-4.0),
 "BF":("Burkina Faso",["burkina faso","ouagadougou"],12.2,-1.6),
 "NE":("Niger",["niger ","niamey","nigerien"],17.6,8.1),
 "TD":("Chad",["chad","n'djamena"],15.5,18.7),
 "NG":("Nigeria",["nigeria","nigerian","abuja","lagos","boko haram"],9.1,8.7),
 "CD":("DR Congo",["congo","drc","kinshasa","goma","m23"],-4.0,21.8),
 "CF":("Central African Republic",["central african republic","bangui"],6.6,20.9),
 "CM":("Cameroon",["cameroon"],7.4,12.4),
 "MZ":("Mozambique",["mozambique","cabo delgado"],-18.7,35.5),
 "ZA":("South Africa",["south africa","johannesburg","pretoria","cape town"],-30.6,22.9),
 "VE":("Venezuela",["venezuela","venezuelan","caracas","maduro"],6.4,-66.6),
 "CU":("Cuba",["cuba","cuban","havana"],21.5,-77.8),
 "MX":("Mexico",["mexico","mexican","cartel","sinaloa"],23.6,-102.6),
 "HT":("Haiti",["haiti","haitian","port-au-prince"],18.97,-72.3),
 "CO":("Colombia",["colombia","colombian","bogota","bogotá"],4.6,-74.3),
 "PA":("Panama",["panama"],8.5,-80.8),
 "EC":("Ecuador",["ecuador","quito"],-1.8,-78.2),
 "PE":("Peru",["peru","lima"],-9.2,-75.0),
 "BR":("Brazil",["brazil","brazilian","brasilia","lula"],-14.2,-51.9),
 "AR":("Argentina",["argentina","buenos aires","milei"],-38.4,-63.6),
 "CL":("Chile",["chile","santiago"],-35.7,-71.5),
 "BO":("Bolivia",["bolivia","la paz"],-16.3,-63.6),
 "NI":("Nicaragua",["nicaragua","managua"],12.9,-85.2),
 "CA":("Canada",["canada","canadian","ottawa"],56.1,-106.3),
 "GL":("Greenland",["greenland"],71.7,-42.6),
 "US":("United States",["united states","washington","pentagon","white house","u.s.","trump","congress","michigan","texas","california","florida","new york","senate","democrat","republican","fbi","midterm"],38.9,-77.0),
}
AREA = {"UA":"UKR-RUS","RU":"UKR-RUS","IL":"ISR-GAZA","PS":"ISR-GAZA","LB":"LEBANON","SY":"SYRIA","IQ":"IRAQ","IR":"IRAN-GULF",
 "YE":"RED SEA","ER":"RED SEA","SA":"IRAN-GULF","AE":"IRAN-GULF","QA":"IRAN-GULF","KW":"IRAN-GULF","BH":"IRAN-GULF","OM":"IRAN-GULF",
 "JO":"MIDEAST","EG":"MIDEAST","TR":"MIDEAST","PK":"S-ASIA","AF":"S-ASIA","IN":"S-ASIA","BD":"S-ASIA","LK":"S-ASIA","NP":"S-ASIA",
 "CN":"INDOPAC","TW":"INDOPAC","JP":"INDOPAC","PH":"INDOPAC","MM":"INDOPAC","TH":"INDOPAC","KH":"INDOPAC","VN":"INDOPAC","ID":"INDOPAC","MY":"INDOPAC","AU":"INDOPAC",
 "KR":"KOREA","KP":"KOREA","GE":"CAUCASUS","AM":"CAUCASUS","AZ":"CAUCASUS","GL":"ARCTIC","US":"HOMELAND","CA":"HOMELAND"}
for c in ["PL","BY","MD","RO","EE","LV","LT","FI","GB","FR","DE","IT","ES","RS","XK","HU","GR","BG"]: AREA[c]="EUROPE"
for c in ["LY","SD","SS","SO","ET","KE","ML","BF","NE","TD","NG","CD","CF","CM","MZ","ZA"]: AREA[c]="AFRICA"
for c in ["VE","CU","MX","HT","CO","PA","EC","PE","BR","AR","CL","BO","NI"]: AREA[c]="LATAM"
PLACE = {"QA":"QATAR","AE":"UAE","SA":"SAUDI","KW":"KUWAIT","BH":"BAHRAIN","OM":"OMAN","YE":"YEMEN","EG":"EGYPT","TR":"TURKEY",
 "PK":"PAKISTAN","AF":"AFGHAN","IN":"INDIA","TW":"TAIWAN","JP":"JAPAN","PH":"PHIL","MM":"MYANMAR","KR":"S.KOREA","PL":"POLAND",
 "BY":"BELARUS","MD":"MOLDOVA","RO":"ROMANIA","EE":"BALTICS","LV":"BALTICS","LT":"BALTICS","LY":"LIBYA","SD":"SUDAN","SO":"SOMALIA",
 "ET":"ETHIOPIA","ML":"SAHEL","BF":"SAHEL","NE":"SAHEL","TD":"SAHEL","NG":"NIGERIA","CD":"DRC","VE":"VENEZ","CU":"CUBA","MX":"MEXICO",
 "HT":"HAITI","CO":"COLOMBIA","PA":"PANAMA"}
# Sub-area keyword overrides -> (placeCode, lat, lon)
SUBPLACE = [(["west bank","jenin","nablus","ramallah","hebron"],"PS","W.BANK",32.0,35.25),
 (["south china sea","spratly","scarborough","second thomas"],None,"S.C.SEA",12.0,114.0),
 (["black sea"],None,"BLK SEA",43.4,34.0),(["red sea","bab el-mandeb","bab al-mandab"],None,None,16.0,41.0)]
import re
_pat = [(iso, re.compile(r"(?<![a-z])"+re.escape(a.strip())+r"(?![a-z])")) for iso,(n,al,_,__) in COUNTRIES.items() for a in al]
def locate(text):
    t = " "+text.lower()+" "
    counts = {}
    for iso,p in _pat:
        m = p.search(t)
        if m: counts[iso] = min(counts.get(iso, 10**6), m.start())
    sub = None
    for kws,iso,pc,la,lo in SUBPLACE:
        if any(k in t for k in kws): sub=(iso,pc,la,lo,kws); break
    if not counts and not sub: return None
    # earliest mention wins, but deprioritise US if others present
    order = sorted(counts, key=lambda i:(i=="US" and len(counts)>1, counts[i]))
    iso = order[0] if order else (sub[0] if sub else None)
    if sub and sub[0]: iso = sub[0]
    name, al, la, lo = COUNTRIES.get(iso, (None,None,None,None)) if iso else (None,None,None,None)
    region = AREA.get(iso, "GLOBAL") if iso else "GLOBAL"
    place = PLACE.get(iso) if iso else None
    if sub:
        if sub[1]: place = sub[1]
        if sub[1]=="S.C.SEA": region="INDOPAC"
        if sub[1]=="BLK SEA": region="UKR-RUS" if iso in ("UA","RU",None) else region
        if sub[1] is None: region="RED SEA"
        la, lo = sub[2], sub[3]
    if iso=="JO": place=None; region="MIDEAST"
    return {"iso2":iso,"admin1":None,"city":None,"lat":la,"lon":lo,"regionCode":region,"placeCode":place,"_country":name}
