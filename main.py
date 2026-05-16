import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "8257539366:AAE7ghKO7W_euTS_UcP8xu3Mlqio_28RvrQ"
CHAT_ID = "768316753"

URLS = [
    # ---- అన్నీ రాష్ట్రాల & కేంద్ర పబ్లిక్ సర్వీస్ కమిషన్లు (PSCs & SSC) ----
    "https://ssc.gov.in/", "https://upsc.gov.in/", "https://upsc.gov.in/recruitment/recruitment-advertisement",
    "https://www.ibps.in/", "https://portal-psc.ap.gov.in/HomePages/RecruitmentNotifications.aspx",
    "https://websitenew.tgpsc.gov.in/notifications", "https://kpsc.kar.nic.in/indexk.html",
    "https://tnpsc.gov.in/English/DNotification.aspx", "https://www.keralapsc.gov.in/notifications",
    "https://www.keralapsc.gov.in/", "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx", 
    "https://hpsc.gov.in/en-us/Instructions", "https://hssc.gov.in/publicNotice", 
    "https://ppsc.gov.in/TAB/SHOWTABLINKS.ASPX?SHOWTABID=10", "https://rpsc.rajasthan.gov.in/advertisements", 
    "https://sssc.uk.gov.in/recruitment-notification/", "https://jkpsc.nic.in/static/forms/notification.aspx", 
    "https://bpsc.bih.gov.in/advertisement/", "https://jssc.jharkhand.gov.in/notices/advertisements", 
    "https://www.ossc.gov.in/Public/Pages/View_Content.aspx?id=1", "https://psc.wb.gov.in/advertisement.jsp", 
    "https://apsc.nic.in/advt_2025.php#advertisement", "https://mpsc.meghalaya.gov.in/advertisements.html", 
    "https://nssb.nagaland.gov.in/category/recruitment/", "https://spsc.sikkim.gov.in/Advertisement.html", 
    "https://tpsc.tripura.gov.in/notifications", "https://mpsc.mizoram.gov.in/page/advertisement-ng-2025-2026", 
    "https://apssb.nic.in/Index/advertisement", "https://mpsc.gov.in/adv_notification/8", 
    "https://gpsc.gujarat.gov.in/pressrelease", "https://mppsc.mp.gov.in/Advertisement", 
    "https://psc.cg.gov.in/htm/Advertisement.htm", "https://gssc.goa.gov.in/?page_id=1079", 
    "https://www.onlinebssc.com/", "https://www.hssc.gov.in/advertisement", "https://hssc.gov.in/result", 
    "https://hppsc.hp.gov.in/hppsc/content/Index/?qlid=3&Ls_is=38", "https://www.ssckkr.kar.nic.in/Vacancy.htm", 
    "https://www.sscmpr.org/index.php?Page=notices", "https://manipurssc.mn.gov.in/GeneralNotice.aspx", 
    "https://sssb.punjab.gov.in/previous-advertisements/", "https://rssb.rajasthan.gov.in/advertisements", 
    "https://sscsr.gov.in/Indexes/notice", "https://upsssc.gov.in//AllNotifications.aspx", 
    "https://jkssb.nic.in/Advertisement.html", "https://jkssb.nic.in/SelectionList.html", "https://jkssb.nic.in/Whatsnew.html",
    "https://sssb.punjab.gov.in/vacancy-group-b/", "https://sssb.punjab.gov.in/vacancy-group-c/",
    "https://sssb.punjab.gov.in/vacancy-group-d/", "https://sssb.punjab.gov.in/circulars/", 
    "https://csbc.bihar.gov.in/", "https://csbc.bihar.gov.in/Default.htm", "https://csbc.bihar.gov.in/A-BFS.htm",
    "https://csbc.bihar.gov.in/A-HPD.htm", "https://csbc.bihar.gov.in/A-BHG.htm", "https://csbc.bihar.gov.in/A-REP.htm",
    "https://csbc.bihar.gov.in/A-EFC.htm", "https://csbc.bihar.gov.in/A-TRN.htm",
    "https://mppsc.mp.gov.in/", "https://opsc.gov.in/Public/OPSC/Default.aspx",
    "https://www.ssc-cr.org/", "https://www.sscwr.net/", "https://www.sscer.org/", 
    "https://www.sscnwr.org/", "https://cag.gov.in/en/recruitment-notices",
    "https://mpsc.gov.in/home", "https://esb.mp.gov.in/", "https://esb.mp.gov.in/e_default.html",
    "https://esb.mp.gov.in/tacs/tacs_n.htm", "https://esb.mp.gov.in/results/results_n.htm",
    "https://npsc.nagaland.gov.in/", "https://gpssb.gujarat.gov.in/", "https://bpssc.bihar.gov.in/",
    "https://ssbodisha.ac.in/", "https://mpsc.mizoram.gov.in/", "https://sssc.uk.gov.in/",
    "https://jssc.jharkhand.gov.in/", "https://apsche.ap.gov.in/", "https://ojas.gujarat.gov.in/",

    # ---- బ్యాంకులు & ఆర్ధిక సంస్థలు (Banks, Finance & Insurance) ----
    "https://www.acab.bank.in/", "https://www.idbi.bank.in/idbi-bank-careers-current-openings.aspx",
    "https://www.centralbank.bank.in/en/recruitments", "https://centralbank.bank.in/en",
    "https://sbi.co.in/web/careers/current-openings", "https://opportunities.rbi.org.in/Scripts/Vacancies.aspx", 
    "https://www.nabard.org/careers-notices1.aspx", "https://www.sebi.gov.in/sebiweb/about/AboutAction.do?doVacancies=yes", 
    "https://www.pnbindia.in/Recruitments.aspx", "https://pnb.bank.in/", "https://bankofbaroda.bank.in/", 
    "https://www.bankofbaroda.in/career/current-opportunities", "https://www.canarabank.com/english/careers/",
    "https://indianbank.in/departments/careers/", "https://www.unionbankofindia.co.in/english/recruitment.aspx",
    "https://www.unionbankofindia.co.in/en/home", "https://licindia.in/Bottom-Links/careers", 
    "https://www.lichousing.com/", "https://www.newindia.co.in/portal/readMore/Recruitment", 
    "https://uiic.co.in/careers/recruitment", "https://orientalinsurance.org.in/careers", 
    "https://nationalinsurance.nic.co.in/en/recruitments", "https://www.sidbi.in/en/careers", 
    "https://www.eximbankindia.in/careers", "https://irdai.gov.in/careers", 
    "https://www.pfrda.org.in/index1.cshtml?lsid=184", "https://nhb.org.in/en/opportunities-at-nhb/", 
    "https://www.epfindia.gov.in/site_en/Recruitments.php", "https://www.esic.gov.in/recruitments",
    "https://jkb.bank.in/", "https://www.hpscb.bank.in/", "https://www.streenidhi.telangana.gov.in/SNTG/UI/Home.aspx",

    # ---- డిఫెన్స్ & పోలీస్ (Defence & Police Boards) ----
    "https://ddpdoo.gov.in/", "https://ddpdoo.gov.in/en/main/home", "https://www.echs.gov.in/job%20vacancies",
    "https://punjabpolice.gov.in/en/notification/punjab-police-notification/", "https://police.odisha.gov.in/en/sun/recruitment",
    "https://iafrecruitment.edcil.co.in/agniveervayu/index.html", "https://indianairforce.nic.in/",
    "https://slprbassam.in/", "https://rect.crpf.gov.in/", "https://crpf.gov.in/index",
    "https://rectt.bsf.gov.in/", "https://cisfrectt.cisf.gov.in/",
    "https://joinindianarmy.nic.in/default.aspx", "https://www.indianarmy.nic.in/", 
    "https://www.joinindiannavy.gov.in/", "https://www.joinindiannavy.gov.in/en/page/current-events.html",
    "https://recruitment.ssb.gov.in/login", "https://ssb.gov.in/recruitmentHome", "https://ssb.gov.in/",
    "https://tslprb.in/", "https://slprb.ap.gov.in/", "https://ksp.karnataka.gov.in/english",
    "https://uppbpb.gov.in/", "https://prb.wb.gov.in/", "https://tnusrb.tn.gov.in/", 
    "https://ksp-recruitment.in/", "https://police.rajasthan.gov.in/Recruitment.aspx", 
    "https://gujaratpolice.gujarat.gov.in/", "https://keralapolice.gov.in/page/recruitment", 
    "https://mahapolice.gov.in/recruitment/",

    # ---- పబ్లిక్ సెక్టార్, రైల్వేస్ & మౌలిక సదుపాయాలు (PSUs, Railways & Infra) ----
    "https://www.barc.gov.in/careers/recruitment.html", "https://www.iocl.com/apprenticeships",
    "https://www.iocl.com/latest-job-opening", "https://npcilcareers.co.in/MainSiten/DefaultInfo.aspx",
    "https://www.npcil.nic.in/content/289_1_Opportunities.aspx", "https://www.npcil.nic.in/content/916_1_Rajbhasha.aspx",
    "https://www.drdo.gov.in/drdo/en/offerings/vacancies", "https://xn--m1b0a2bb8esed.xn--11b7cb3a6a.xn--h2brj9c/drdo/en/offerings/vacancies",
    "https://www.hindustanpetroleum.com/job-openings", "https://www.bharatpetroleum.in/index",
    "https://www.tgtransco.com/index.php/what-s-new-3", "https://www.ecil.co.in/jobopenings",
    "https://bescom.karnataka.gov.in/#", "https://gsrtc.in/site/downloads/innerPages/recruitment.html",
    "https://scr.indianrailways.gov.in/", "https://scr.onlineregister.org.in/home",
    "https://www.rrbapply.gov.in/", "https://www.rrbapply.gov.in/#/auth/landing", "https://aweil.in/", "https://rrbsecunderabad.gov.in/",
    "https://rrbbilaspur.gov.in/", "https://secr.indianrailways.gov.in/view_section.jsp?lang=0&id=0,2,1903,219", "https://secr.indianrailways.gov.in/?lan",
    "https://rlda.indianrailways.gov.in/", "https://www.isro.gov.in/Careers.html", "https://fci.gov.in/personnel.php?view=333", 
    "https://ongcindia.com/web/eng/career/recruitment-notice", "https://careers.ntpc.co.in/", 
    "https://www.ntpc.co.in/", "https://www.ntpc.co.in/jobs-ntpc",
    "https://careers.bhel.in/", "https://gailonline.com/CRApplyingGail.html",
    "https://sailcareers.com/", "https://hal-india.co.in/Career_Details.aspx",
    "https://www.coalindia.in/career-cil/", "https://www.coalindia.in/", "https://www.mahanadicoal.in/",
    "https://bel-india.in/CareersGridbind.aspx", "https://bdl-india.in/careers", 
    "https://midhani-india.in/department_name/hrd-careers/", "https://www.powergrid.in/job-opportunities", 
    "https://www.powergrid.in/", "https://www.rites.com/vacancies",
    "https://scclmines.com/scclnew/careers_Notification.asp", "https://www.apgenco.co.in/home/careers",
    "https://nhai.gov.in/#/vacancies", "https://nhai.gov.in/#/", "https://www.bsnl.co.in/opencms/bsnl/BSNL/about_us/hrd/jobs.html",
    "https://www.nmdc.co.in/careers", "https://www.nmdc.co.in/", "https://www.vizagsteel.com/myindex.asp?tm=9&url=code/tenders/viewjobadds.asp",
    "https://www.irctc.com/human-resources.html", "https://concorindia.co.in/careers.asp",
    "https://www.nhpcindia.com/career", "https://www.nhpcindia.com/", "https://sjvn.nic.in/career",
    "https://www.ircon.org/index.php?lang=english&page=careers", "https://www.rvnl.org/rvnl-careers", 
    "https://www.brahmos.com/careers.php", "https://www.meconlimited.co.in/career.aspx", "https://www.meconlimited.co.in/",
    "https://www.hudco.org.in/careers", "https://uidai.gov.in/en/about-uidai/work-with-uidai.html",
    "https://www.iffco.in/en/corporate", "https://www.gujaratmetrorail.com/", "https://opalindia.in/",
    "https://alimco.in/", "https://recruitment.eil.co.in/", "https://www.oil-india.com/advertisement-list",
    "https://fact.co.in/home/Dynamicpages?MenuId=90", "https://engineersindia.com/", "https://hrrl.in/Hrrl/home.jsp",

    # ---- విద్యుత్ సంస్థలు (State Power Boards) ----
    "https://www.uppcl.org/uppcl/en/article/vacancyresults", "https://www.tangedco.gov.in/hr-recruitment.html",
    "https://kptcl.karnataka.gov.in/english", "https://www.mahadiscom.in/en/careers/",
    "https://energy.rajasthan.gov.in/rvpnl/#/home/career", "https://www.gsecl.in/careers",
    "https://wbsetcl.in/career.html", "https://www.bspcl.co.in/Employment.aspx",
    "https://optcl.co.in/View/Careers.aspx", "https://kseb.in/index.php/careers",
    "https://pspcl.in/", "https://cescmysore.karnataka.gov.in/", "https://gescom.karnataka.gov.in/",

    # ---- యూనివర్సిటీలు, IITs & విద్యా సంస్థలు (Universities, IITs, NITs) ----
    "https://keralacseb.kerala.gov.in/?cat=98", "https://keralacseb.kerala.gov.in/?cat=100",
    "https://www.nitt.edu/home/other/jobs/group_bc_recruitment_2026/", "https://www.nitt.edu/home/other/jobs/faculty_recruitment_2026/",
    "https://www.nitt.edu/home/other/jobs/group_a_2026/", "https://www.nitt.edu/home/other/jobs/previous/",
    "https://www.vnsgu.ac.in/recruitment.html", "https://dmer.maharashtra.gov.in/english/advertisement-2025-26/teaching-contractual/",
    "https://dmer.maharashtra.gov.in/english/advertisement-2025-26/non-teaching-contractual/",
    "https://sanskrit.nic.in/recruitments_notifications.php", 
    "https://navodaya.gov.in/nvs/en/Recruitment/Notification-Vacancies/", "https://navodaya.gov.in/nvs/en/Home1/",
    "https://navodaya.gov.in/nvs/nvs-school/CHANDIGARH", "https://kvsangathan.nic.in/employment-notice/", 
    "https://www.iitb.ac.in/en/careers/staff-recruitment", "https://home.iitd.ac.in/jobs-iitd/index.php", "https://www.iitm.ac.in/notices", 
    "https://www.iitkgp.ac.in/non-teaching-positions", "https://www.iitk.ac.in/new/recruitment", 
    "https://iitr.ac.in/Careers/index.html", "https://nitw.ac.in/path/?dept=/jobs", 
    "https://www.nitk.ac.in/careers", "https://www.uohyd.ac.in/careers-uoh/", 
    "https://www.jnu.ac.in/career", "https://www.bhu.ac.in/Site/RecruitmentInfo",
    "https://www.sggu.ac.in/", "https://www.du.ac.in/", "https://www.msubaroda.ac.in/",
    "https://cetonline.karnataka.gov.in/kea/", "https://graupunjab.org/", "https://digital.gndu.ac.in/", "https://cau.ac.in/",

    # ---- మెడికల్, AIIMS & హెల్త్ బోర్డులు (Medical, AIIMS & State Health Boards) ----
    "https://www.aiims.edu/en/notices/recruitment/aiims-recruitment.html", "https://jipmer.edu.in/announcement/jobs",
    "https://aiimsbhubaneswar.nic.in/Recruitment_Notice.aspx", "https://aiimsrishikesh.edu.in/a1_1/?page_id=2753",
    "https://aiimsbibinagar.edu.in/recruitment/", "https://aiimsmangalagiri.edu.in/vacancy/",
    "https://pgimer.edu.in/PGIMER_PORTAL/PGIMERPORTAL/home.jsp", "https://nimhans.ac.in/vacancy-announcements/",
    "https://cfw.ap.nic.in/Recruitments.html", "https://www.mrb.tn.gov.in/notifications.html", 
    "https://upnrhm.gov.in/Home/Vacancies", "https://statehealth.bihar.gov.in/careers.html", 
    "https://arogyakeralam.gov.in/careers/", "https://nrhm.maharashtra.gov.in/vacancies.htm", 
    "https://wbhealth.gov.in/pages/career", "https://rajswasthya.nic.in/", 
    "https://nhm.gujarat.gov.in/recruitment.htm",

    # ---- కోర్టులు & రీసెర్చ్ సంస్థలు (Courts, Research, Ports & Aviation) ----
    "https://main.sci.gov.in/recruitment", "https://tshc.gov.in/HighCourt/Notifications",
    "https://aphc.gov.in/recruitment", "https://hckrecruitment.keralacourts.in/",
    "https://karnatakajudiciary.kar.nic.in/recruitment.php", "https://judiciary.karnataka.gov.in/",
    "https://bombayhighcourt.nic.in/recruitment.php", "https://delhihighcourt.nic.in/open_position", 
    "https://www.mhc.tn.gov.in/recruitment/login", "https://www.csir.res.in/career-opportunities/recruitment", 
    "https://main.icmr.nic.in/career-opportunity", "https://www.icar.org.in/content/vacancy", 
    "https://iisc.ac.in/positions-open/", "https://www.cdac.in/index.aspx?id=current_jobs", 
    "https://nielit.gov.in/recruitments", "https://www.prl.res.in/prl-eng/opportunities/job", 
    "https://www.bose.res.in/recruitment/", "https://www.icfre.gov.in/recruitment", 
    "https://fri.icfre.gov.in/recruitment-01/", "https://tiho.org.in/careers", 
    "https://www.niot.res.in/index.php/recruitment", "https://www.aai.aero/en/careers/recruitment", 
    "https://mazagondock.in/Career-Executive.aspx", "https://cochinshipyard.in/career", 
    "https://www.grse.in/job-opportunities/", "https://goashipyard.in/careers/advertisement/", 
    "https://www.chennaiport.gov.in/careers", "https://www.mptgoa.gov.in/careers/", 
    "https://vpt.ap.nic.in/Careers.aspx", "https://www.syama-prasad-mookerjee-port-kolkata.gov.in/careers", 
    "https://www.pawanahans.co.in/career.aspx", "https://www.aaiclas.aero/",

    # ---- ఇతర బోర్డులు, మున్సిపల్ కార్పొరేషన్లు & సబార్డినేట్ సర్వీసెస్ (Other Subordinate Boards) ----
    "https://upbocw.in/English/index.aspx", "https://sswcd.punjab.gov.in/en/advertisement-for-recruitment-of-aww-awh-and-state-commissioner",
    "https://www.kmcgov.in/KMCPortal/jsp/Recruitment2015.jsp", "https://www.kmcgov.in/KMCPortal/jsp/KMCResult2015.jsp",
    "https://jrhms.jharkhand.gov.in/Career/List", "https://ossc.gov.in/Public/OSSC/Default.aspx",
    "https://sundargarh.odisha.gov.in/en/notices/notifications", "https://sundargarh.odisha.gov.in/en/notice/results",
    "https://sundargarh.odisha.gov.in/en/notice/recruitment", "https://gsssb.gujarat.gov.in/News/Index", 
    "https://gsssb.gujarat.gov.in/Index", "https://gsssb.gujarat.gov.in/Notification", "https://dsssb.delhi.gov.in/notifications", 
    "https://portal.centralselectionboard.com/notice/", "https://rural.assam.gov.in/", 
    "https://nmmc.gov.in/additional-content/Jobs", "https://csc.gov.in/careers", 
    "https://www.suratmunicipal.gov.in/Information/RecruitmentDashboard", "https://hmda.gov.in/notifications.aspx", 
    "https://www.cgg.gov.in/careers/", "https://www.indiapost.gov.in/VAS/Pages/Content/Recruitments.aspx", 
    "https://www.ncs.gov.in/Pages/default.aspx", "https://rsmssb.rajasthan.gov.in/page?menuName=ApBuI6wdvnNKC6MoOgFsfXwFRsE7cKXQ", 
    "https://btsc.bih.nic.in/", "https://bssc.bihar.gov.in/Home", "https://uksssc.uk.gov.in/", 
    "https://wbhrb.in/", "https://osssc.gov.in/Public/OSSSC/Default.aspx", "https://mssb.mizoram.gov.in/",
    "https://andamannicobar.gov.in/", "https://forest.tripura.gov.in/", "https://bmcgujarat.com/", 
    "https://ahmedabadcity.gov.in/", "https://upanganwadibharti.in/", 
    "https://tribal.maharashtra.gov.in/Site/Home/Index.aspx", "https://www.pcmcindia.gov.in/", 
    "https://ramgarh.nic.in/", "https://www.upcisb.upsdc.gov.in/", "https://wii.gov.in/",

    # ---- మన తెలుగు రాష్ట్రాల స్పెషల్ సంస్థలు (AP & TS Exclusives) ----
    "https://mhsrb.telangana.gov.in/MHSRB/home.htm", "https://www.tsrtc.telangana.gov.in/vacancies.php",
    "https://www.apsrtc.ap.gov.in/recruitments.aspx", "https://apspdcl.in/careers.jsp",
    "https://www.apcpdcl.in/careers", "https://www.tssouthernpower.com/careers",
    "https://tsnpdcl.in/careers", "https://www.singarenicolleries.com/careers/",
    "https://hmwseb.telangana.gov.in/careers", "https://www.sweroes.org/careers",
    "https://treirb.telangana.gov.in/", "https://tgtwgurukulam.telangana.gov.in/recruitments"
]

MEMORY_FILE = "bot_memory.txt"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_memory(fname):
    with open(MEMORY_FILE, "a") as f:
        f.write(fname + "\n")

def get_clean_filename(url):
    path = urlparse(url).path
    return os.path.basename(path)

def monitor():
    print("GitHub Action Scanning Started... 🚀")
    sent_filenames = load_memory()
    is_first_run = len(sent_filenames) == 0
    
    # ఎర్రర్స్ వచ్చి ఓపెన్ కాని సైట్స్ ని సేవ్ చేసుకోవడానికి లిస్ట్ 
    failed_urls = [] 

    for url in URLS:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')

            new_updates = []
            for a in soup.find_all('a', href=True):
                full_url = urljoin(url, a['href'])
                fname = get_clean_filename(full_url)

                if any(ext in fname.lower() for ext in ['.pdf', '.html', '.aspx']) and fname not in sent_filenames:
                    if len(fname) > 5:
                        if not is_first_run: 
                            new_updates.append(full_url)
                        sent_filenames.add(fname)
                        save_memory(fname)

            if new_updates:
                links_text = "\n".join(new_updates[:5])
                alert = f"📢 <b>కొత్త నోటిఫికేషన్!</b>\n\n<b>సైట్:</b> {url}\n\n<b>లింక్స్:</b>\n{links_text}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": alert, "parse_mode": "HTML"})

        except Exception as e:
            print(f"Skipping {url} due to timeout/error.")
            # ఓపెన్ కాని సైట్ ని మన లిస్ట్ లోకి యాడ్ చేస్తున్నాం
            failed_urls.append(url)
            continue
        
        time.sleep(1)

    # ---- స్కిప్ అయిన సైట్స్ లిస్ట్ ని టెలిగ్రామ్ కి పంపడం ----
    if failed_urls:
        print(f"Sending {len(failed_urls)} failed URLs to Telegram...")
        
        # టెలిగ్రామ్ మెసేజ్ లిమిట్ దాటకుండా, ప్రతి 30 లింక్స్ ని ఒక మెసేజ్ లా పంపుతున్నాం
        chunk_size = 30
        for i in range(0, len(failed_urls), chunk_size):
            chunk = failed_urls[i:i+chunk_size]
            failed_msg = "\n".join(chunk)
            alert_msg = f"⚠️ <b>స్కిప్ అయిన సైట్స్ (Failed URLs) - Part {i//chunk_size + 1}:</b>\n\n{failed_msg}"
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": alert_msg, "parse_mode": "HTML"})
            time.sleep(2) # మెసేజ్ బ్లాక్ అవ్వకుండా 2 సెకన్ల గ్యాప్

    print("Scanning complete. Exiting successfully. ✅")

if __name__ == "__main__":
    monitor()
