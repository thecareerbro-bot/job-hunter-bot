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
    "https://ssc.gov.in/", "https://upsc.gov.in/recruitment/recruitment-advertisement",
    "https://www.ibps.in/", "https://portal-psc.ap.gov.in/HomePages/RecruitmentNotifications.aspx",
    "https://websitenew.tgpsc.gov.in/notifications", "https://kpsc.kar.nic.in/indexk.html",
    "https://tnpsc.gov.in/English/DNotification.aspx", "https://www.keralapsc.gov.in/notifications",
    "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx", "https://hpsc.gov.in/en-us/Instructions",
    "https://hssc.gov.in/publicNotice", "https://ppsc.gov.in/TAB/SHOWTABLINKS.ASPX?SHOWTABID=10",
    "https://rpsc.rajasthan.gov.in/advertisements", "https://sssc.uk.gov.in/recruitment-notification/",
    "https://jkpsc.nic.in/static/forms/notification.aspx", "https://bpsc.bih.gov.in/advertisement/",
    "https://jssc.jharkhand.gov.in/notices/advertisements", "https://www.ossc.gov.in/Public/Pages/View_Content.aspx?id=1",
    "https://psc.wb.gov.in/advertisement.jsp", "https://apsc.nic.in/advt_2025.php#advertisement",
    "https://mpsc.meghalaya.gov.in/advertisements.html", "https://nssb.nagaland.gov.in/category/recruitment/",
    "https://spsc.sikkim.gov.in/Advertisement.html", "https://tpsc.tripura.gov.in/notifications",
    "https://mpsc.mizoram.gov.in/page/advertisement-ng-2025-2026", "https://apssb.nic.in/Index/advertisement",
    "https://mpsc.gov.in/adv_notification/8", "https://gpsc.gujarat.gov.in/pressrelease",
    "https://mppsc.mp.gov.in/Advertisement", "https://psc.cg.gov.in/htm/Advertisement.htm",
    "https://gssc.goa.gov.in/?page_id=1079", "https://www.onlinebssc.com/",
    "https://www.hssc.gov.in/advertisement", "https://hppsc.hp.gov.in/hppsc/content/Index/?qlid=3&Ls_is=38",
    "https://www.ssckkr.kar.nic.in/Vacancy.htm", "https://www.sscmpr.org/index.php?Page=notices",
    "https://manipurssc.mn.gov.in/GeneralNotice.aspx", "https://sssb.punjab.gov.in/previous-advertisements/",
    "https://rssb.rajasthan.gov.in/advertisements", "https://sscsr.gov.in/Indexes/notice",
    "https://upsssc.gov.in//AllNotifications.aspx", "https://jkssb.nic.in/Advertisement.html",
    "https://sssb.punjab.gov.in/vacancy-group-b/", "https://sssb.punjab.gov.in/vacancy-group-c/",
    "https://sssb.punjab.gov.in/vacancy-group-d/", "https://hssc.gov.in/advertisement",
    "https://hssc.gov.in/result", "https://csbc.bihar.gov.in/", "https://sssb.punjab.gov.in/circulars/",
    "https://www.acab.bank.in/", "https://upsc.gov.in/", "https://ddpdoo.gov.in/",
    "https://ssbodisha.ac.in/", "https://mppsc.mp.gov.in/", "https://opsc.gov.in/Public/OPSC/Default.aspx",
    "https://www.barc.gov.in/careers/recruitment.html", "https://hprca.hp.gov.in/advertisements",
    "https://keralacseb.kerala.gov.in/?cat=98", "https://keralacseb.kerala.gov.in/?cat=100",
    "https://www.echs.gov.in/job%20vacancies", "https://www.idbi.bank.in/idbi-bank-careers-current-openings.aspx",
    "https://punjabpolice.gov.in/en/notification/punjab-police-notification/", "https://upbocw.in/English/index.aspx",
    "https://police.odisha.gov.in/en/sun/recruitment", "https://sswcd.punjab.gov.in/en/advertisement-for-recruitment-of-aww-awh-and-state-commissioner",
    "https://www.nitt.edu/home/other/jobs/group_bc_recruitment_2026/", "https://www.nitt.edu/home/other/jobs/faculty_recruitment_2026/",
    "https://www.nitt.edu/home/other/jobs/group_a_2026/", "https://www.nitt.edu/home/other/jobs/previous/",
    "https://www.kmcgov.in/KMCPortal/jsp/Recruitment2015.jsp", "https://www.kmcgov.in/KMCPortal/jsp/KMCResult2015.jsp",
    "https://jrhms.jharkhand.gov.in/Career/List", "https://ossc.gov.in/Public/OSSC/Default.aspx",
    "https://www.centralbank.bank.in/en/recruitments", "https://esb.mp.gov.in/e_default.html",
    "https://esb.mp.gov.in/tacs/tacs_n.htm", "https://esb.mp.gov.in/results/results_n.htm",
    "https://sundargarh.odisha.gov.in/en/notices/notifications", "https://sundargarh.odisha.gov.in/en/notice/results",
    "https://sundargarh.odisha.gov.in/en/notice/recruitment", "https://www.iocl.com/apprenticeships",
    "https://www.iocl.com/latest-job-opening", "https://jkssb.nic.in/SelectionList.html",
    "https://jkssb.nic.in/Whatsnew.html", "https://npcilcareers.co.in/MainSiten/DefaultInfo.aspx",
    "https://www.npcil.nic.in/content/289_1_Opportunities.aspx", "https://www.npcil.nic.in/content/916_1_Rajbhasha.aspx",
    "https://www.drdo.gov.in/drdo/en/offerings/vacancies", "https://www.vnsgu.ac.in/recruitment.html",
    "https://gsssb.gujarat.gov.in/News/Index", "https://gsssb.gujarat.gov.in/Notification",
    "https://dsssb.delhi.gov.in/notifications", "https://iafrecruitment.edcil.co.in/agniveervayu/index.html",
    "https://portal.centralselectionboard.com/notice/", "https://www.hindustanpetroleum.com/job-openings",
    "https://csbc.bihar.gov.in/Default.htm", "https://csbc.bihar.gov.in/A-BFS.htm",
    "https://csbc.bihar.gov.in/A-HPD.htm", "https://csbc.bihar.gov.in/A-BHG.htm",
    "https://csbc.bihar.gov.in/A-REP.htm", "https://csbc.bihar.gov.in/A-EFC.htm",
    "https://csbc.bihar.gov.in/A-TRN.htm", "https://rural.assam.gov.in/",
    "https://www.tgtransco.com/index.php/what-s-new-3", "https://www.ecil.co.in/jobopenings",
    "https://nmmc.gov.in/additional-content/Jobs", "https://dmer.maharashtra.gov.in/english/advertisement-2025-26/teaching-contractual/",
    "https://dmer.maharashtra.gov.in/english/advertisement-2025-26/non-teaching-contractual/",
    "https://slprbassam.in/", "https://bescom.karnataka.gov.in/#", "https://csc.gov.in/careers",
    "https://gsrtc.in/site/downloads/innerPages/recruitment.html",
    "https://scr.indianrailways.gov.in/",
    "https://scr.onlineregister.org.in/home",
    "https://www.suratmunicipal.gov.in/Information/RecruitmentDashboard",
    "https://aweil.in/",
    "https://www.rrbapply.gov.in/",
    "https://recruitment.ssb.gov.in/login",
    "https://ssb.gov.in/recruitmentHome",
    "https://ssb.gov.in/"
    "https://sanskrit.nic.in/recruitments_notifications.php"

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

    for url in URLS:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            # 15 సెకన్ల టైమ్-అవుట్ సెట్ చేశాం. ఓపెన్ అవ్వకపోతే వదిలేసి తర్వాతి సైట్‌కి వెళ్తుంది.
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
            continue
        
        # బ్లాక్ అవ్వకుండా, ఒక్కో సైట్‌కి మధ్య 1 సెకను గ్యాప్
        time.sleep(1)

    print("Scanning complete. Exiting successfully. ✅")

if __name__ == "__main__":
    monitor()
