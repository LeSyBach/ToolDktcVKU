import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import os
import sys
from datetime import datetime

# ═══════════════════════════════════════════════
#   TOOL ĐĂNG KÝ TÍN CHỈ VKU — V7.0 ULTIMATE
#   Author: @LÊ SỸ BÁCH
# ═══════════════════════════════════════════════

class C:
    RESET  = "\033[0m";  BOLD   = "\033[1m"
    GREEN  = "\033[92m"; YELLOW = "\033[93m"
    RED    = "\033[91m"; CYAN   = "\033[96m"
    BLUE   = "\033[94m"; MAGENTA= "\033[95m"
    WHITE  = "\033[97m"; DIM    = "\033[2m"
    BG_DARK= "\033[40m"

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(C.CYAN + C.BOLD)
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║   ██╗   ██╗██╗  ██╗██╗   ██╗    ██████╗ ██╗  ██╗   ║")
    print("  ║   ██║   ██║██║ ██╔╝██║   ██║    ██╔══██╗██║ ██╔╝   ║")
    print("  ║   ██║   ██║█████╔╝ ██║   ██║    ██║  ██║█████╔╝    ║")
    print("  ║   ╚██╗ ██╔╝██╔═██╗ ██║   ██║    ██║  ██║██╔═██╗    ║")
    print("  ║    ╚████╔╝ ██║  ██╗╚██████╔╝    ██████╔╝██║  ██╗   ║")
    print("  ║     ╚═══╝  ╚═╝  ╚═╝ ╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ║")
    print("  ║                                                      ║")
    print("  ║         TOOL ĐĂNG KÝ TÍN CHỈ  ─  v7.0              ║")
    print("  ║                                                      ║")
    print("  ║  " + C.YELLOW + "Author : @LÊ SỸ BÁCH" + C.CYAN + "                             ║")
    print("  ║  " + C.GREEN  + "Status : READY (ULTIMATE PAIRING MODE)" + C.CYAN + "             ║")
    print("  ║  " + C.DIM    + "Build  : CLI Edition — VKU Student Tool" + C.CYAN + "              ║")
    print("  ║                                                      ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(C.RESET)

def divider(title="", char="─", width=56):
    if title:
        pad = (width - len(title) - 2) // 2
        print(C.DIM + "  " + char*pad + " " + C.CYAN + C.BOLD + title + C.DIM + " " + char*(width-pad-len(title)-2) + C.RESET)
    else:
        print(C.DIM + "  " + char*width + C.RESET)

def ok(msg):    print(f"  {C.GREEN}{C.BOLD}[✓]{C.RESET} {msg}")
def err(msg):   print(f"  {C.RED}{C.BOLD}[✗]{C.RESET} {msg}")
def info(msg):  print(f"  {C.CYAN}[i]{C.RESET} {msg}")
def warn(msg):  print(f"  {C.YELLOW}[!]{C.RESET} {msg}")
def wait(msg):  print(f"  {C.MAGENTA}[~]{C.RESET} {msg}", end='\r')

def prompt(msg, default=None):
    suffix = f" [{C.DIM}{default}{C.RESET}]" if default else ""
    val = input(f"  {C.YELLOW}»{C.RESET} {msg}{suffix}: ").strip()
    return val if val else default

def nhap_cookie():
    divider("NHẬP COOKIE")
    print(f"  {C.DIM}Mở trình duyệt → F12 → Network → chọn request bất kỳ → tab Headers → copy giá trị{C.RESET}\n")

    xsrf = prompt("Dán giá trị XSRF-TOKEN")
    if not xsrf:
        err("XSRF-TOKEN trống! Thoát."); sys.exit(1)
    xsrf = xsrf.strip()
    if xsrf.lower().startswith("xsrf-token="): xsrf = xsrf[len("xsrf-token="):]

    print()
    session = prompt("Dán giá trị laravel_session")
    if not session:
        err("laravel_session trống! Thoát."); sys.exit(1)
    session = session.strip()
    if session.lower().startswith("laravel_session="): session = session[len("laravel_session="):]

    cookie = f"XSRF-TOKEN={xsrf}; laravel_session={session}"
    print()
    ok(f"XSRF-TOKEN    : {C.DIM}{xsrf[:32]}...{C.RESET}")
    ok(f"laravel_session: {C.DIM}{session[:32]}...{C.RESET}")
    return cookie

# ═══════════════════════════════
#   CORE LOGIC
# ═══════════════════════════════

class VKUTool:
    def __init__(self, cookie, base_url="https://daotao.vku.udn.vn"):
        self.base_url = base_url
        self.headers  = {'User-Agent': 'Mozilla/5.0', 'Cookie': cookie}
        self.dang_ky_ok = set()
        self.lock = threading.Lock()
        self.debug = False

    def get(self, url, timeout=8):
        try:
            return requests.get(url, headers=self.headers, timeout=timeout)
        except Exception as e:
            err(f"Lỗi kết nối: {e}")
            return None

    def lay_danh_sach_mon(self):
        res = self.get(f"{self.base_url}/sv/dang-ky-tin-chi")
        if not res: return []
        soup = BeautifulSoup(res.text, 'html.parser')
        mons = []
        for row in soup.find_all('tr'):
            btn = row.find('button', class_='xem')
            if btn:
                tds = row.find_all('td')
                ten = tds[2].text.strip() if len(tds) > 2 else '???'
                mons.append({'id': btn['data-id'], 'ten': ten, 'ds_lop': []})
        return mons

    def lay_ds_lop(self, hocphan_id):
        res = self.get(f"{self.base_url}/sv/tin-chi-xem-chi-tiet?id={hocphan_id}")
        if not res: return []
        soup = BeautifulSoup(res.text, 'html.parser')
        lops = []
        for link in soup.find_all('a', href=lambda x: x and 'dang-ky-tung-lophp' in x):
            try:
                idlop = link['href'].split('idlop=')[1].split('&')[0]
                
                # --- PHẦN SỬA LỖI CHÍNH ---
                row = link.find_parent('tr') # Tìm ngược lên cái hàng (row) chứa nút Chọn
                if not row: continue
                
                tds = row.find_all('td') # Lấy tất cả các cột trong hàng đó
                
                # Cột thứ 2 (index 1) chính là Tên Lớp Học Phần (theo đúng HTML của bạn)
                ten_lop = tds[1].text.strip() if len(tds) > 1 else idlop
                
                # Sĩ số ở cột 3 (index 2), Lịch học ở cột 6 (index 5)
                si_so = tds[2].text.strip() if len(tds) > 2 else '?'
                lich  = tds[5].text.strip() if len(tds) > 5 else '?'
                
                lops.append({'idlop': idlop, 'ten_lop': ten_lop, 'si_so': si_so, 'lich': lich})
            except: continue
        return lops

    def dang_ky_lop(self, hocphan_id, idlop, ten_mon="?", debug=False):
        with self.lock:
            if hocphan_id in self.dang_ky_ok:
                return 'skip'
        url = f"{self.base_url}/sv/dang-ky-tung-lophp?hocphan_id={hocphan_id}&idlop={idlop}&m=100"
        res = self.get(url)
        if not res: return 'error'

        raw  = res.text
        text = raw.lower()
        code = res.status_code
        
        if debug or getattr(self, 'debug', False):
            print(f"\n  {C.DIM}[DEBUG] HTTP {code} | {len(raw)} bytes{C.RESET}")

        SUCCESS_KW = ["thành công", "đã lưu", "đăng ký thành", "đã đăng ký", "\"status\":1", "\"code\":1"]
        FAIL_KW = ["hết chỗ", "đầy", "trùng lịch", "không thể", "không được", "alert-danger", "alert-warning"]

        is_success = any(k in text for k in SUCCESS_KW)
        is_fail    = any(k in text for k in FAIL_KW)

        if is_success or (code == 200 and not is_fail and len(raw.strip()) < 80):
            with self.lock:
                self.dang_ky_ok.add(hocphan_id)
            ok(f"{C.BOLD}THÀNH CÔNG{C.RESET}: {ten_mon} — Lớp {idlop}")
            return 'ok'

        if is_fail: return 'fail'
        
        if code == 200 and not is_fail:
            with self.lock:
                self.dang_ky_ok.add(hocphan_id)
            ok(f"{C.BOLD}THÀNH CÔNG{C.RESET} (Bypass HTTP 200): {ten_mon}")
            return 'ok'
        return 'unknown'

# ═══════════════════════════════
#   MENU + LUỒNG CHỨC NĂNG
# ═══════════════════════════════

def menu_chinh():
    banner()
    divider("MENU CHÍNH")
    print(f"  {C.CYAN}1.{C.RESET}  Quét MÔN học → Chọn môn")
    print(f"  {C.CYAN}2.{C.RESET}  Quét LỚP HỌC PHẦN → Chọn thủ công")
    print(f"  {C.CYAN}3.{C.RESET}  Nhập cặp {C.YELLOW}MÔN:LỚP{C.RESET} (Tốc độ ánh sáng, chuẩn 100%)")
    print(f"  {C.CYAN}4.{C.RESET}  {C.YELLOW}⏰ HẸN GIỜ SNIPE{C.RESET} — Khóa mục tiêu trước, chờ mở cửa là bắn")
    print(f"  {C.CYAN}5.{C.RESET}  {C.RED}{C.BOLD}🚀 BẮN THẲNG BẰNG ID (KHÔNG QUÉT - NHANH NHẤT){C.RESET}")
    print(f"  {C.CYAN}0.{C.RESET}  Thoát\n")
    divider()
    chon = prompt("Chọn chức năng (0-5)")
    return chon

# --- (Chức năng 1 & 2 giữ nguyên logic cũ, thu gọn để nhường chỗ cho 3 & 4) ---
def chuc_nang_1(tool):
    divider("CHẾ ĐỘ 1 — QUÉT MÔN HỌC")
    info("Đang tải danh sách môn...")
    mons = tool.lay_danh_sach_mon()

    if not mons:
        err("Không có môn nào. Kiểm tra cookie.")
        input("\n  [Enter để quay lại]")
        return

    print()
    for i, m in enumerate(mons):
        print(f"  {C.CYAN}{i+1:02d}.{C.RESET} {m['ten']}  {C.DIM}(ID: {m['id']}){C.RESET}")

    print()
    chon_raw = prompt("Nhập số thứ tự môn muốn đăng ký (vd: 1,3,5 hoặc all)")

    if not chon_raw or not chon_raw.strip():
        err("Bạn chưa nhập môn nào.")
        input("\n  [Enter để quay lại]")
        return

    chon_raw = chon_raw.strip()

    if chon_raw.lower() == 'all':
        ds_chon = [m['id'] for m in mons]
    else:
        try:
            ds_chon = []
            for x in chon_raw.split(','):
                x = x.strip()
                if not x:
                    continue

                idx = int(x) - 1

                if idx < 0 or idx >= len(mons):
                    err(f"Số thứ tự không hợp lệ: {x}")
                    input("\n  [Enter để quay lại]")
                    return

                ds_chon.append(mons[idx]['id'])

            if not ds_chon:
                err("Không có môn hợp lệ để đăng ký.")
                input("\n  [Enter để quay lại]")
                return

        except ValueError:
            err("Nhập không hợp lệ. Ví dụ đúng: 1,3,5 hoặc all")
            input("\n  [Enter để quay lại]")
            return

    _chay_dang_ky_list(tool, ds_chon, mons)

    input("\n  [Enter để quay lại menu]")


# ── Lựa chọn 2: Quét môn → xem TẤT CẢ LỚP → chọn lớp cụ thể ──
def chuc_nang_2(tool):
    divider("CHẾ ĐỘ 2 — QUÉT LỚP HỌC PHẦN")
    info("Đang tải danh sách môn...")
    mons = tool.lay_danh_sach_mon()
    if not mons:
        err("Không lấy được dữ liệu."); input("\n  [Enter]"); return

    for i, m in enumerate(mons):
        print(f"  {C.CYAN}{i+1:02d}.{C.RESET} {m['ten']}  {C.DIM}({m['id']}){C.RESET}")

    print()
    idx = prompt("Chọn môn để xem các lớp (số thứ tự)")
    try:
        mon = mons[int(idx)-1]
    except:
        err("Không hợp lệ"); input("\n  [Enter]"); return

    divider(f"LỚP CỦA: {mon['ten']}")
    info(f"Đang tải danh sách lớp...")
    lops = tool.lay_ds_lop(mon['id'])

    if not lops:
        warn("Không tìm thấy lớp nào."); input("\n  [Enter]"); return

    print()
    for i, l in enumerate(lops):
        siso_str = f"{C.DIM}Sĩ số: {l['si_so']}{C.RESET}" if l['si_so'] != '?' else ''
        lich_str = f"  {C.DIM}{l['lich']}{C.RESET}" if l['lich'] != '?' else ''
        print(f"  {C.CYAN}{i+1:02d}.{C.RESET} [{C.YELLOW}{l['ten_lop']}{C.RESET}]  ID:{l['idlop']}  {siso_str}{lich_str}")

    print()
    chon_raw = prompt("Chọn lớp muốn đăng ký (vd: 1,2 hoặc all)")
    if chon_raw.strip().lower() == 'all':
        ds_lop_chon = lops
    else:
        try:
            ds_lop_chon = [lops[int(x.strip())-1] for x in chon_raw.split(',')]
        except:
            err("Không hợp lệ"); input("\n  [Enter]"); return

    divider("BẮT ĐẦU ĐĂNG KÝ")
    for l in ds_lop_chon:
        wait(f"Đang đăng ký lớp {l['ten_lop']} ...")
        res = tool.dang_ky_lop(mon['id'], l['idlop'], mon['ten'], debug=getattr(tool,"debug",False))
        if res == 'ok':
            break
        elif res == 'fail':
            warn(f"Lớp {l['ten_lop']} chưa thành công — thử lớp tiếp...")
        elif res == 'skip':
            info("Môn này đã đăng ký thành công trước đó."); break

    input("\n  [Enter để quay lại]")

# ── Lựa chọn 3: Tối ưu Cặp Môn:Lớp (ÉP CHUỖI TUYỆT ĐỐI) ──
def chuc_nang_3(tool):
    divider("CHẾ ĐỘ 3 — CÚ PHÁP KÉP MÔN:LỚP")
    print(f"  {C.DIM}Cú pháp: Tên Môn : Tên Lớp. Cách nhau bởi dấu phẩy (,){C.RESET}")
    print(f"  {C.DIM}Ví dụ: Triết học Mác - Lênin: Triết học Mác - Lênin (1), Lập trình: Lập trình (2){C.RESET}\n")

    raw = prompt("Nhập danh sách")
    if not raw or not raw.strip(): return
    
    # Tách chuỗi thành các cặp (Môn, Lớp)
    pairs = []
    for item in raw.split(','):
        if ':' in item:
            m, l = item.split(':', 1)
            pairs.append((m.strip(), l.strip()))
        else:
            warn(f"Bỏ qua '{item.strip()}' vì thiếu dấu ':'")
            
    if not pairs:
        err("Không có cặp Môn:Lớp nào hợp lệ!"); input("\n  [Enter]"); return

    info("Đang lấy danh sách môn mới nhất...")
    mons = tool.lay_danh_sach_mon()
    if not mons:
        err("Không lấy được danh sách môn. Kiểm tra Cookie."); input("\n  [Enter]"); return

    ds_hop_le = []
    for mon_nhap, lop_nhap in pairs:
        mon_clean = mon_nhap.lower().replace(" ", "")
        lop_clean = lop_nhap.lower().replace(" ", "")
        
        # 1. Khóa mục tiêu Môn Học
        matched_mon = None
        for m in mons:
            m_clean = m['ten'].lower().replace(" ", "")
            if m_clean == mon_clean or mon_clean in m_clean or m_clean in mon_clean:
                matched_mon = m
                break
                
        if not matched_mon:
            err(f"Không tìm thấy môn học nào khớp với: '{mon_nhap}'")
            continue
            
        # 2. Khóa mục tiêu Lớp Học
        lops_cua_mon = tool.lay_ds_lop(matched_mon['id'])
        matched_lop = None
        for l in lops_cua_mon:
            l_clean = l['ten_lop'].lower().replace(" ", "")
            idlop_clean = l['idlop'].lower().replace(" ", "")
            if l_clean == lop_clean or lop_clean in l_clean or idlop_clean == lop_clean:
                matched_lop = l
                break
                
        if matched_lop:
            ok(f"Đã khóa: {C.BOLD}{matched_mon['ten']}{C.RESET} 🎯 Lớp: {C.YELLOW}{matched_lop['ten_lop']}{C.RESET}")
            ds_hop_le.append({
                'hocphan_id': matched_mon['id'],
                'idlop': matched_lop['idlop'],
                'ten_mon': matched_mon['ten'],
                'ten_lop': matched_lop['ten_lop']
            })
        else:
            err(f"Môn '{matched_mon['ten']}' không có lớp nào khớp với '{lop_nhap}'")

    if not ds_hop_le:
        input("\n  [Enter để quay lại]"); return

    print()
    xac_nhan = prompt(f"Xác nhận khai hỏa {len(ds_hop_le)} lớp này? (y/n)", default="y")
    if xac_nhan.lower() != 'y': return

    _chay_dang_ky_lop_specific(tool, ds_hop_le)

# ── Lựa chọn 4: Hẹn giờ Snipe (Hỗ trợ cú pháp Môn:Lớp) ──
def chuc_nang_4(tool):
    divider("CHẾ ĐỘ 4 — HẸN GIỜ SNIPE")
    print(f"  {C.DIM}Lưu trước các cặp Môn:Lớp. Chờ hệ thống mở là bóp cò ngay!{C.RESET}\n")

    gio_str = prompt("Nhập giờ mở đăng ký (định dạng HH:MM:SS, vd: 07:00:00)")
    ngay_str = prompt("Nhập ngày (YYYY-MM-DD, trống = hôm nay)", default="")

    try:
        now = datetime.now()
        if ngay_str:
            target = datetime.strptime(f"{ngay_str} {gio_str}", "%Y-%m-%d %H:%M:%S" if len(gio_str)==8 else "%Y-%m-%d %H:%M")
        else:
            fmt = "%H:%M:%S" if len(gio_str)==8 else "%H:%M"
            t = datetime.strptime(gio_str, fmt)
            target = now.replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
    except:
        err("Thời gian không hợp lệ."); input("\n  [Enter]"); return

    som_str = prompt("Khởi động sớm trước bao nhiêu giây?", default="1")
    som = int(som_str) if som_str.isdigit() else 1
    target_fire = target.timestamp() - som

    ok(f"Mục tiêu: {target.strftime('%Y-%m-%d %H:%M:%S')} (kích hoạt sớm {som}s)")

    print()
    divider("CHỌN CHẾ ĐỘ SNIPE")
    print(f"  {C.CYAN}1.{C.RESET} Quét tất cả môn → Đăng ký Vét Cạn (Lớp đầu tiên còn chỗ)")
    print(f"  {C.CYAN}2.{C.RESET} Khai báo TÊN MÔN : TÊN LỚP → Chỉ bắn mục tiêu chuẩn xác\n")
    mode = prompt("Chọn (1/2)", default="1")

    pairs = []
    if mode == '2':
        raw = prompt("Nhập danh sách Môn:Lớp (cách nhau dấu ,)")
        for item in raw.split(','):
            if ':' in item:
                m, l = item.split(':', 1)
                pairs.append((m.strip(), l.strip()))
        ok(f"Đã ghi nhớ {len(pairs)} cặp mục tiêu. Sẽ truy quét ID ngay khi trường mở!")

    divider("ĐẾM NGƯỢC")
    try:
        while True:
            now_ts = time.time()
            diff = target_fire - now_ts
            if diff <= 0: break
            h, m, s = int(diff // 3600), int((diff % 3600) // 60), int(diff % 60)
            pulse = "●" if int(diff) % 2 == 0 else "○"
            sys.stdout.write(f"\r  {C.YELLOW}{pulse}{C.RESET} Còn lại: {C.CYAN}{C.BOLD}{h:02d}:{m:02d}:{s:02d}{C.RESET} → Khai hỏa lúc {target.strftime('%H:%M:%S')}   ")
            sys.stdout.flush()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n  {C.YELLOW}Đã hủy hẹn giờ.{C.RESET}"); input("\n  [Enter để quay lại]"); return

    print(f"\n\n  {C.GREEN}{C.BOLD}🔥 ĐÃ ĐẾN GIỜ MỞ CỬA — BẮT ĐẦU TRUY QUÉT HỆ THỐNG!{C.RESET}\n")

    mons_moi_nhat = tool.lay_danh_sach_mon()
    if not mons_moi_nhat:
        err("Không lấy được dữ liệu. Có thể do nghẽn mạng hoặc sai Cookie.")
        input("\n  [Enter để quay lại]"); return

    if mode == '2' and pairs:
        ds_hop_le = []
        for mon_nhap, lop_nhap in pairs:
            mon_clean, lop_clean = mon_nhap.lower().replace(" ", ""), lop_nhap.lower().replace(" ", "")
            matched_mon = next((m for m in mons_moi_nhat if m['ten'].lower().replace(" ", "") == mon_clean or mon_clean in m['ten'].lower().replace(" ", "")), None)
            
            if matched_mon:
                lops_cua_mon = tool.lay_ds_lop(matched_mon['id'])
                matched_lop = next((l for l in lops_cua_mon if l['ten_lop'].lower().replace(" ", "") == lop_clean or lop_clean in l['ten_lop'].lower().replace(" ", "")), None)
                if matched_lop:
                    ok(f"BẮT ĐƯỢC: {matched_mon['ten']} - {matched_lop['ten_lop']} (ID: {matched_lop['idlop']})")
                    ds_hop_le.append({
                        'hocphan_id': matched_mon['id'], 'idlop': matched_lop['idlop'],
                        'ten_mon': matched_mon['ten'], 'ten_lop': matched_lop['ten_lop']
                    })
                else:
                    warn(f"Hệ thống mở nhưng KHÔNG TÌM THẤY LỚP: {lop_nhap}")
            else:
                warn(f"Hệ thống mở nhưng KHÔNG TÌM THẤY MÔN: {mon_nhap}")

        if ds_hop_le:
            _chay_dang_ky_lop_specific(tool, ds_hop_le)
        else:
            input("\n  [Enter để quay lại]")
    else:
        ids = [m['id'] for m in mons_moi_nhat]
        _chay_dang_ky_list(tool, ids, mons_moi_nhat)

# ── Lựa chọn 5: Bắn thẳng bằng ID (Không quét web) ──
def chuc_nang_5(tool):
    divider("CHẾ ĐỘ 5 — BẮN BẰNG ID (TỐC ĐỘ SIÊU TỐC)")
    print(f"  {C.DIM}Cách lấy ID: Chuột phải vào nút [Đăng ký] trên web -> Copy link.{C.RESET}")
    print(f"  {C.DIM}Link có dạng: ...hocphan_id=871&idlop=20053...{C.RESET}\n")

    hpid = prompt("Nhập ID Môn học (hocphan_id, vd: 871)")
    idlop = prompt("Nhập ID Lớp học phần (idlop, vd: 20053)")
    
    if not hpid or not idlop: return

    divider("ĐANG BÓP CÒ...")
    def fire():
        res = tool.dang_ky_lop(hpid.strip(), idlop.strip(), "Môn Chỉ Định VIP")
        if res == 'fail': time.sleep(0.1)

    with ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(lambda x: fire(), range(5))

    print()
    if hpid.strip() in tool.dang_ky_ok:
        ok(f"QUÁ NHANH QUÁ NGUY HIỂM! Đã ghim thành công vào lớp {idlop}.")
    else:
        warn("Lớp đã full hoặc bị khóa.")
    
    input(f"\n  {C.CYAN}>> Nhấn [Enter] để quay lại menu...{C.RESET}")

# ── Helper: Chạy đăng ký cho TÊN LỚP CHỈ ĐỊNH ──
def _chay_dang_ky_lop_specific(tool, ds_lop):
    divider("BẮT ĐẦU BẮN LỚP CHỈ ĐỊNH")
    def xu_ly(lop):
        if lop['hocphan_id'] in tool.dang_ky_ok: return
        res = tool.dang_ky_lop(lop['hocphan_id'], lop['idlop'], lop['ten_mon'])
        if res == 'fail': time.sleep(0.1)

    with ThreadPoolExecutor(max_workers=15) as ex:
        ex.map(xu_ly, ds_lop)

    print()
    divider("KẾT QUẢ CUỐI CÙNG")
    ok(f"Đã đăng ký thành công: {C.BOLD}{len(tool.dang_ky_ok)}{C.RESET} môn")
    input(f"\n  {C.CYAN}>> Nhấn [Enter] để quay lại menu chính...{C.RESET}")

# ── Helper: Chạy đăng ký VÉT CẠN ──
def _chay_dang_ky_list(tool, ds_id, mons):
    divider("BẮT ĐẦU CHIẾN DỊCH VÉT CẠN")
    ten_map = {m['id']: m['ten'] for m in mons}

    def xu_ly(hpid):
        lops = tool.lay_ds_lop(hpid)
        for l in lops:
            if hpid in tool.dang_ky_ok: break
            res = tool.dang_ky_lop(hpid, l['idlop'], ten_map.get(hpid, hpid))
            if res == 'ok': break
            if res == 'fail': time.sleep(0.1)

    with ThreadPoolExecutor(max_workers=15) as ex:
        ex.map(xu_ly, ds_id)

    print()
    divider("KẾT QUẢ CUỐI CÙNG")
    ok(f"Đã đăng ký thành công: {C.BOLD}{len(tool.dang_ky_ok)}{C.RESET} môn")
    failed = set(ds_id) - tool.dang_ky_ok
    if failed: warn(f"Chưa đăng ký được: {len(failed)} môn")
    input(f"\n  {C.CYAN}>> Nhấn [Enter] để quay lại menu chính...{C.RESET}")

# ═══════════════════════════════
#   ENTRY POINT
# ═══════════════════════════════

def main():
    debug = '--debug' in sys.argv
    banner()
    if debug: print(f"  {C.YELLOW}[DEBUG MODE ON]{C.RESET} — sẽ in response thô khi đăng ký\n")
    cookie = nhap_cookie()
    tool = VKUTool(cookie)
    tool.debug = debug
    print()

    while True:
        chon = menu_chinh()
        if   chon == '1': chuc_nang_1(tool)
        elif chon == '2': chuc_nang_2(tool)
        elif chon == '3': chuc_nang_3(tool)
        elif chon == '4': chuc_nang_4(tool)
        elif chon == '5': chuc_nang_5(tool)
        elif chon == '0':
            banner()
            ok("Tạm biệt! Chúc Bách đăng ký tín chỉ thành công 🎉")
            divider()
            sys.exit(0)
        else:
            warn("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
