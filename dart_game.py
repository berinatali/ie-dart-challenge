import json
import math
import os
import random
import time
import tkinter as tk
from tkinter import font as tkfont

# =====================================================================
#  SORU HAVUZU  (250+ soru)
#  Her satır: (soru, DOĞRU cevap, yanlış 1, yanlış 2, yanlış 3, ipucu)
#  Kendi sorunu eklemek için aynı formatta yeni bir satır ekle.
# =====================================================================
_RAW = [
    # ---------------- ENVANTER VE ÜRETİM PLANLAMA ----------------
    ("EOQ modelinin amacı nedir?", "Toplam sipariş ve stok tutma maliyetini minimize eden sipariş miktarını bulmak", "Satışları maksimize etmek", "İşçi sayısını azaltmak", "Makine hızını artırmak", "Sipariş verme ve stok tutma maliyetleri dengelenir."),
    ("Ekonomik sipariş miktarı (EOQ) formülü hangisidir?", "√(2DS/H)", "√(DS/2H)", "2DS/H", "√(2HS/D)", "D yıllık talep, S sipariş maliyeti, H birim stok tutma maliyetidir."),
    ("MRP kısaltmasının açılımı nedir?", "Malzeme İhtiyaç Planlaması", "Makine Rotasyon Planı", "Maliyet Raporlama Programı", "Montaj Rotası Planlaması", "Hangi malzemeden ne zaman ne kadar gerektiğini hesaplar."),
    ("MRP sisteminin temel girdilerinden biri hangisidir?", "Ürün ağacı (BOM)", "Çalışan maaş listesi", "Reklam bütçesi", "Müşteri şikayetleri", "Ürünün hangi parçalardan oluştuğunu gösterir."),
    ("Ürün ağacı (BOM) neyi gösterir?", "Bir ürünün bileşenlerini ve miktarlarını hiyerarşik olarak", "Ürünün satış fiyatını", "İşçilerin vardiya planını", "Makinelerin bakım takvimini", "Ürünün hangi parçalardan, kaçar adet oluştuğunu söyler."),
    ("Ana Üretim Çizelgesi (MPS) neyi belirler?", "Hangi nihai ürünün ne zaman ve ne kadar üretileceğini", "Çalışanların izin günlerini", "Tedarikçi ödemelerini", "Reklam kampanyasını", "Nihai ürünler için zaman-miktar planıdır."),
    ("Toplu üretim planlaması (aggregate planning) hangi vadeyi kapsar?", "Orta vadeli üretim, işgücü ve stok planını", "Anlık makine ayarını", "Günlük vardiya devrini", "Yalnızca satın alma sözleşmesini", "Genelde 3-18 aylık planlama ufkudur."),
    ("Emniyet stoku neden tutulur?", "Talep ve tedarik süresi belirsizliğine karşı korunmak için", "Vergi ödememek için", "Depoyu doldurmak için", "Fiyatları artırmak için", "Belirsizliğe karşı tampon görevi görür."),
    ("Yeniden sipariş noktası (ROP) neye eşittir?", "Tedarik süresi boyunca talep + emniyet stoku", "Yıllık talep / 12", "Sipariş maliyeti × talep", "Ortalama stok × 2", "Stok bu seviyeye düşünce sipariş verilir."),
    ("Stok devir hızı nasıl hesaplanır?", "Satılan malın maliyeti / ortalama stok değeri", "Ortalama stok / satılan malın maliyeti", "Toplam satış / çalışan sayısı", "Net kâr / toplam varlık", "Stoğun yılda kaç kez yenilendiğini gösterir."),
    ("ABC analizinde A grubu kalemler hangisidir?", "Sayıca az, değerce yüksek kalemler", "Sayıca çok, değerce düşük kalemler", "Hiç hareket etmeyen kalemler", "Sadece hammaddeler", "Yakından kontrol edilmesi gereken kritik kalemlerdir."),
    ("ABC analizi hangi ilkeye dayanır?", "Pareto (80/20) ilkesine", "Little yasasına", "Murphy yasasına", "Moore yasasına", "Az sayıdaki kalem değerin büyük kısmını oluşturur."),
    ("Elde bulundurma maliyetine hangisi girer?", "Depolama, sigorta ve sermayenin fırsat maliyeti", "Sipariş formu hazırlama maliyeti", "Makine kurulum (setup) maliyeti", "Eksik stok cezası", "Stoğu elde tutmanın bedelidir."),
    ("Eksik stok (stockout) maliyeti nedir?", "Talebin karşılanamamasından doğan kayıp", "Depo kirası", "Sipariş verme maliyeti", "Makine amortismanı", "Müşteri kaybı ve satış kaybını içerir."),
    ("Back order (gecikmeli sipariş) ne demektir?", "Stokta olmayan ürünün sonradan teslim edilmek üzere kaydedilmesi", "Siparişin iptali", "Fazla üretilen ürün", "Müşteriden ürün iadesi", "Talep kaybolmaz, ileri tarihte karşılanır."),
    ("Newsvendor (gazete satıcısı) modeli neyi çözer?", "Tek dönemlik, belirsiz talepli stok miktarı kararını", "Ağdaki en kısa yolu", "Atama problemini", "Hat dengelemeyi", "Satılmayan ürünün değeri düşer, tek sipariş verilir."),
    ("Servis seviyesi neyi ifade eder?", "Talebin stoktan karşılanma olasılığını", "Çalışan memnuniyetini", "Makine kullanım oranını", "İndirim oranını", "Müşteri talebinin stoktan karşılanma yüzdesidir."),
    ("(Q, R) stok politikasında ne olur?", "Stok R seviyesine düşünce Q birim sipariş verilir", "Her ay sabit Q sipariş verilir", "Stok hiç tutulmaz", "Yılda bir kez sipariş verilir", "Sürekli gözden geçirme sistemidir."),
    ("Periyodik gözden geçirme sisteminde ne yapılır?", "Stok belirli aralıklarla kontrol edilip hedef seviyeye tamamlanır", "Stok sıfır olunca sipariş verilir", "Hiç sipariş verilmez", "Yalnızca yıllık sipariş verilir", "Kontrol zamanı sabittir, sipariş miktarı değişir."),
    ("Wagner-Whitin algoritması neyi çözer?", "Dinamik talepli çok dönemli parti büyüklüğü problemini", "Ağda en kısa yolu", "Atama problemini", "Gezgin satıcı problemini", "Dinamik programlama ile parti büyüklüğü belirler."),
    ("Tedarik süresi (lead time) nedir?", "Sipariş verilmesinden teslimata kadar geçen süre", "Üretim hattının uzunluğu", "Günlük çalışma saati", "Stok devir süresi", "Sipariş ile teslim arasındaki bekleme süresi."),
    ("Döngüsel sayım (cycle counting) nedir?", "Stokların yıl boyunca parça parça sayılması", "Yılda bir kez tüm depoyu sayma", "Siparişlerin iptali", "Üretim hızının ölçülmesi", "Sürekli ve küçük gruplar halinde sayım yapılır."),
    ("Stok tutmanın bir amacı hangisidir?", "Üretim ile talep arasındaki dengesizliği tamponlamak", "Müşteriyi beklettirmek", "Vergiyi artırmak", "Depo alanını boşaltmak", "Stok bir tampon görevi görür."),
    ("Çapraz sevkiyat (cross-docking) nedir?", "Malların depolanmadan doğrudan sevkiyata aktarılması", "Malların uzun süre saklanması", "Üretimin durdurulması", "Siparişin iptali", "Gelen mal depoda beklemeden çıkış aracına geçer."),
    ("Parti büyüklüğü (lot size) büyüdükçe ne olur?", "Sipariş sayısı azalır, stok tutma maliyeti artar", "Her iki maliyet de azalır", "Sipariş sayısı artar", "Stok düşer", "Sipariş ve stok maliyeti birbirinin tersine hareket eder."),

    # ---------------- KALİTE ----------------
    ("PERT analizi CPM'den hangi yönüyle ayrılır?", "Olasılıksal süre tahminleri kullanması", "Sadece inşaatta kullanılması", "Bilgisayara ihtiyaç duyması", "Maliyeti dikkate almaması", "PERT, belirsizlik için beta dağılımı gibi olasılıksal süreler kullanır."),
    ("Altı Sigma metodolojisinin hedefi nedir?", "Milyonda 3.4 hata oranına ulaşmak", "Hata oranını %50 yapmak", "Üretimi tamamen durdurmak", "Maliyeti iki katına çıkarmak", "Süreç varyansını azaltarak kusursuzluğa odaklanır."),
    ("Kontrol kartlarını ilk kim geliştirmiştir?", "Walter Shewhart", "Henry Ford", "Frederick Taylor", "Max Weber", "İstatistiksel kalite kontrolün öncüsü, Bell Labs araştırmacısıdır."),
    ("DMAIC'in açılımı nedir?", "Tanımla, Ölç, Analiz Et, İyileştir, Kontrol Et", "Tasarla, Üret, Analiz Et, Dağıt, Kontrol Et", "Durdur, Ölç, Ayarla, İncele, Çıkar", "Dene, Mühendislik, Ara, İzle, Cevapla", "Altı Sigma'nın beş aşamalı problem çözme döngüsüdür."),
    ("Pareto diyagramı nedir?", "Sorunları sıklığına göre azalan sırada gösteren çubuk grafik", "Zaman serisi çizgi grafiği", "Neden-sonuç diyagramı", "İki değişkenin dağılım grafiği", "Az sayıdaki nedenin çok sorun yarattığını gösterir."),
    ("Balık kılçığı (Ishikawa) diyagramı ne işe yarar?", "Bir sorunun olası nedenlerini kategorilere ayırır", "Ürün maliyetini hesaplar", "Sipariş akışını gösterir", "Kritik yolu bulur", "Neden-sonuç diyagramı olarak da bilinir."),
    ("X-bar ve R kontrol kartları hangi tür veri için kullanılır?", "Sürekli (ölçülebilir) veri", "Sayılabilir kusur verisi", "Sadece nitel veri", "Sıralı kategorik veri", "Uzunluk, ağırlık gibi ölçümler için kullanılır."),
    ("p kontrol kartı neyi izler?", "Hatalı ürün oranını", "Ortalama ölçüyü", "Ölçü aralığını", "Üretim hızını", "Kusurlu birimlerin oranı için kullanılır."),
    ("c kontrol kartı neyi izler?", "Bir birimdeki kusur sayısını", "Hatalı ürün yüzdesini", "Ortalama ağırlığı", "Standart sapmayı", "Birim başına kusur sayısı Poisson dağılır."),
    ("Cp süreç yeterlilik indeksi neyi ifade eder?", "Spesifikasyon genişliğinin süreç yayılımına oranını", "Süreç ortalamasını", "Hata sayısını", "Üretim hızını", "Cp = (USL − LSL) / 6σ"),
    ("Cpk, Cp'den hangi yönüyle ayrılır?", "Süreç ortalamasının merkezden kaymasını da dikkate alır", "Maliyeti hesaba katar", "Hızı ölçer", "Örnek büyüklüğünü değiştirir", "Ortalamanın spesifikasyon sınırlarına yakınlığına bakar."),
    ("ISO 9001 hangi alanda bir standarttır?", "Kalite yönetim sistemi", "Çevre yönetimi", "İş sağlığı ve güvenliği", "Bilgi güvenliği", "Müşteri memnuniyeti ve süreç yaklaşımı odaklıdır."),
    ("ISO 14001 hangi alanda bir standarttır?", "Çevre yönetim sistemi", "Kalite yönetimi", "Enerji verimliliği", "Gıda güvenliği", "Çevresel performansı yönetmek içindir."),
    ("Toplam Kalite Yönetimi (TQM) neyi savunur?", "Tüm çalışanların katıldığı sürekli iyileştirmeyi", "Yalnızca son kontrolü", "Sadece maliyet düşürmeyi", "Satış artırmayı", "Kalite herkesin sorumluluğudur."),
    ("PDCA döngüsünün açılımı nedir?", "Planla, Uygula, Kontrol Et, Önlem Al", "Tasarla, Üret, Denetle, Sat", "Planla, Üret, Sat, Kapat", "Dene, Düzelt, Çalıştır, Ara", "Deming döngüsü olarak da bilinir."),
    ("Kaizen ne anlama gelir?", "Sürekli küçük adımlarla iyileştirme", "Ani büyük yenilik", "Stok azaltma", "Fiyat artırma", "Japonca 'iyi değişim' anlamındadır."),
    ("Poka-yoke nedir?", "Hataların oluşmasını önleyen hataya dayanıklı tasarım", "Hızlı üretim tekniği", "Stok kontrol yöntemi", "Maliyet hesaplama", "Yanlış parçanın takılmasını imkânsız kılan basit düzenekler."),
    ("FMEA nedir?", "Hata türleri ve etkileri analizi", "Finansal maliyet analizi", "Zaman etüdü yöntemi", "Fayda-maliyet raporu", "Olası hataları önceden belirleyip önceliklendirir."),
    ("FMEA'da RPN nasıl hesaplanır?", "Şiddet × Oluşma × Tespit edilebilirlik", "Şiddet + Oluşma + Tespit", "Şiddet / Oluşma", "Oluşma + Tespit", "Üç puanın çarpımıdır."),
    ("Kabul örneklemesi nedir?", "Bir partiyi kabul/ret kararı için örnek inceleme", "Tüm ürünlerin %100 muayenesi", "Üretim hızı ölçümü", "Fiyat belirleme", "Partiden çekilen örneğe bakarak karar verilir."),
    ("OC (işletme karakteristik) eğrisi neyi gösterir?", "Partinin kabul olasılığını kusur oranına göre", "Maliyet değişimini", "İşçi sayısını", "Zaman ilişkisini", "Örnekleme planının ayırt etme gücünü gösterir."),
    ("Kalite maliyetleri hangi gruplardan oluşur?", "Önleme, değerlendirme, iç hata ve dış hata", "Hammadde ve işçilik", "Reklam ve satış", "Kira ve vergi", "Önleme-değerlendirme-hata sınıflaması kullanılır."),
    ("Dayanıklı (robust) tasarım ve kalite kayıp fonksiyonu kime aittir?", "Genichi Taguchi", "Walter Shewhart", "Taiichi Ohno", "Henry Gantt", "Japon kalite mühendisi."),
    ("Kalite çemberleri nedir?", "Gönüllü çalışanların sorun çözdüğü küçük gruplar", "Üst yönetim kurulu", "Dış denetim ekibi", "Tedarikçi toplantısı", "Çalışanlar iş sorunlarını birlikte çözer."),
    ("Histogram neyi gösterir?", "Verilerin frekans dağılımını", "Neden-sonuç ilişkisini", "Kritik yolu", "Zaman serisini", "Veri aralıklarındaki gözlem sayısını gösteren çubuk grafiktir."),
    ("Juran'ın kalite trilojisi hangisidir?", "Kalite planlama, kontrol ve iyileştirme", "Maliyet, süre ve kapsam", "Girdi, süreç ve çıktı", "Tasarım, üretim ve satış", "Joseph Juran'a aittir."),

    # ---------------- YALIN ÜRETİM ----------------
    ("Yalın üretimin temel amacı nedir?", "İsrafı ortadan kaldırarak değer yaratmak", "Stoku artırmak", "İşçi sayısını azaltmak", "Fiyatı yükseltmek", "Müşterinin değer vermediği her şey israftır."),
    ("Toyota Üretim Sistemi'nin mimarı kimdir?", "Taiichi Ohno", "Henry Ford", "Frederick Taylor", "Walter Shewhart", "Toyota'da çalışan bir mühendis."),
    ("Hangisi yalın üretimin 7 israfından biridir?", "Aşırı üretim", "Pazarlama", "Eğitim", "Yenilik", "Gereğinden fazla üretmek israfların başında gelir."),
    ("5S'in ilk adımı olan Seiri neyi ifade eder?", "Ayıklama (gereksizleri ayırma)", "Temizlik", "Standartlaştırma", "Disiplin", "Çalışma alanındaki gereksizler ayrılır."),
    ("5S'te Seiton ne demektir?", "Düzenleme (her şeyin bir yeri olması)", "Ayıklama", "Temizlik", "Disiplin", "Gereken şey kolay bulunacak yerde durur."),
    ("Çekme (pull) sisteminde üretimi ne tetikler?", "Gerçek müşteri talebi", "Satış tahmini", "Sürekli stok hedefi", "Fazla üretim planı", "İhtiyaç olmadan üretim yapılmaz."),
    ("Kanban nedir?", "Üretim ve malzeme akışını sinyalleyen kart/görsel sistem", "Kalite kontrol grafiği", "Maliyet yöntemi", "Tahmin tekniği", "Japonca 'kart' anlamına gelir."),
    ("Değer akış haritalama (VSM) ne işe yarar?", "Malzeme ve bilgi akışını görselleştirip israfı bulur", "Maliyeti hesaplar", "İş planı hazırlar", "Tesis yeri seçer", "Başlangıçtan teslimata tüm akışı gösterir."),
    ("Takt time nedir?", "Müşteri talebini karşılamak için gereken üretim hızı", "Bir ürünün çevrim süresi", "Tedarik süresi", "Makine bakım süresi", "Kullanılabilir süre / talep."),
    ("SMED yöntemi neyi hedefler?", "Ayar/kalıp değiştirme sürelerini kısaltmayı", "Stok azaltmayı", "Kaliteyi ölçmeyi", "Personel almayı", "Tek haneli dakikada ayar değişimi hedeflenir."),
    ("Heijunka ne demektir?", "Üretimi dengeleme (düzleştirme)", "Kalite kontrol", "Satış tahmini", "Tedarikçi seçimi", "Üretim çeşit ve miktarı dengeli dağıtılır."),
    ("Jidoka ilkesi nedir?", "Hata olunca makinenin otomatik durması", "Aşırı üretim", "Stok biriktirme", "Müşteri anketi", "Otonomasyon: insan zekâsı katılmış otomasyon."),
    ("Andon nedir?", "Üretimdeki sorunu gösteren görsel/sesli sinyal sistemi", "Maliyet raporu", "Stok kartı", "Zaman ölçer", "Sorun olunca ışık yanar, hat durabilir."),
    ("Gemba kavramı neyi ifade eder?", "Değerin yaratıldığı gerçek yer (üretim sahası)", "Yönetim ofisi", "Bilgi işlem odası", "Muhasebe", "Japonca 'gerçek yer' demektir."),
    ("Genchi Genbutsu ne demektir?", "Gidip yerinde görmek", "Stok yapmak", "Raporu okumak", "Maliyeti kısmak", "Sorunu anlamak için sahaya gidilir."),
    ("TPM kısaltması neyi ifade eder?", "Toplam Verimli Bakım", "Toplam Planlı Pazarlama", "Teknik Personel Eğitimi", "Tam Üretim Modeli", "Operatörlerin de bakıma katıldığı yaklaşım."),
    ("OEE nasıl hesaplanır?", "Kullanılabilirlik × Performans × Kalite", "Kullanılabilirlik + Performans", "Hız / Hata", "Maliyet × Süre", "Ekipman verimliliğinin üç çarpanı vardır."),
    ("Japoncada 'muda' ne anlama gelir?", "İsraf", "Disiplin", "Kalite", "Yük", "Yalın düşüncenin en temel kavramıdır."),
    ("Hücresel üretim nedir?", "Benzer parçaları grup halinde işleyen hücreler kurmak", "Tek makinede her şeyi üretmek", "Sadece montaj hattı kurmak", "Atölye tipi düzen", "Grup teknolojisi esasına dayanır."),
    ("WIP kısaltması neyi ifade eder?", "Süreçteki iş (yarı mamul)", "Haftalık stok planı", "Çalışma talimatı", "Üretim projeksiyonu", "Work In Process."),

    # ---------------- YÖNEYLEM ARAŞTIRMASI ----------------
    ("Doğrusal programlama nedir?", "Doğrusal kısıtlar altında doğrusal amaç fonksiyonunu optimize etme", "Rastgele sayı üretme", "Kuyruk analizi", "Talep tahmini", "Kâr maksimizasyonu veya maliyet minimizasyonu için kullanılır."),
    ("Simplex yöntemi neyi çözer?", "Doğrusal programlama problemlerini", "Kuyruk problemlerini", "Tahmin hatalarını", "Stok problemlerini", "Köşe noktalar arasında ilerleyen bir algoritmadır."),
    ("Simplex algoritmasını geliştiren kişi kimdir?", "George Dantzig", "Edsger Dijkstra", "Andrey Markov", "John Little", "1947'de geliştirilmiştir."),
    ("Doğrusal programlamada fizibil bölge nedir?", "Tüm kısıtları sağlayan çözümler kümesi", "Sadece optimum nokta", "Hatalı çözümler", "Boş küme", "Kabul edilebilir çözümlerin bölgesidir."),
    ("Gölge fiyat (shadow price) neyi gösterir?", "Bir kısıtın sağ tarafındaki bir birim artışın amaç fonksiyonuna etkisini", "Ürünün satış fiyatını", "Vergi oranını", "İşçi ücretini", "Kaynağın marjinal değeridir."),
    ("Atama problemi hangi yöntemle çözülür?", "Macar (Hungarian) yöntemi", "Newton yöntemi", "Gauss eliminasyonu", "Monte Carlo", "İş-kaynak eşleştirmesi için kullanılır."),
    ("Ulaştırma problemi neyi amaçlar?", "Arz noktalarından talep noktalarına taşıma maliyetini minimize etmek", "Kritik yolu bulmak", "Stok seviyesini belirlemek", "Hatları dengelemek", "Kaynak-hedef akışları optimize edilir."),
    ("Kuzeybatı köşe yöntemi ne için kullanılır?", "Ulaştırmada başlangıç çözümü bulmak", "Kuyruk modeli çözmek", "Tahmin yapmak", "Simülasyon kurmak", "Tablonun sol üst köşesinden başlanır."),
    ("Tamsayılı programlamada karar değişkenleri nasıldır?", "Tamsayı değer almak zorundadır", "Sürekli olmalıdır", "Rastgele olmalıdır", "Negatif olmalıdır", "Örneğin makine veya kişi sayısı kesirli olamaz."),
    ("Dal-sınır (branch and bound) yöntemi neyi çözer?", "Tamsayılı programlama problemlerini", "Zaman serisi tahminlerini", "Kontrol kartlarını", "Hat dengelemeyi", "Çözüm uzayını dallara ayırıp eler."),
    ("Dinamik programlamanın kurucusu kimdir?", "Richard Bellman", "George Dantzig", "A. K. Erlang", "Vilfredo Pareto", "Bellman optimalite ilkesini ortaya koymuştur."),
    ("Bellman'ın optimalite ilkesi ne söyler?", "Optimal politikanın alt politikaları da optimaldir", "Her zaman açgözlü seçilmelidir", "Kısıtlar silinmelidir", "Rastgele seçim yapılmalıdır", "Problem aşamalara bölünerek çözülür."),
    ("Dijkstra algoritması neyi bulur?", "Ağda en kısa yolu", "Minimum kapsayan ağacı", "Maksimum akışı", "En iyi atamayı", "Negatif olmayan ağırlıklı ağlarda çalışır."),
    ("Kruskal algoritması neyi bulur?", "Minimum kapsayan ağacı", "En kısa yolu", "Maksimum akışı", "Kritik yolu", "Tüm düğümleri en az toplam maliyetle bağlar."),
    ("Maksimum akış-minimum kesim teoremi neyi söyler?", "Maksimum akış, minimum kesim kapasitesine eşittir", "Akış her zaman sıfırdır", "Kesim akıştan küçüktür", "Akış rastgeledir", "Ford-Fulkerson teoremidir."),
    ("Gezgin satıcı problemi nedir?", "Tüm şehirleri birer kez gezip dönen en kısa turu bulmak", "En fazla akışı bulmak", "Stok belirlemek", "İşleri atamak", "Zor (NP-zor) bir rota problemidir."),
    ("Karar ağacı ne işe yarar?", "Kararları ve olası sonuçlarını olasılıklarla modeller", "Kritik yolu bulur", "Stok hesaplar", "Hat dengeler", "Belirsizlik altında karar vermeye yardımcı olur."),
    ("Mahkûm ikilemi hangi alana aittir?", "Oyun teorisi", "Kuyruk teorisi", "Stok teorisi", "Zaman etüdü", "Bireysel rasyonellik ortak kötü sonuç doğurabilir."),
    ("Oyun teorisinin öncülerinden biri kimdir?", "John von Neumann", "Frederick Taylor", "Henry Gantt", "Taiichi Ohno", "Morgenstern ile birlikte kitap yazmıştır."),
    ("Nash dengesi nedir?", "Hiçbir oyuncunun tek başına stratejisini değiştirerek kazanç sağlayamadığı durum", "Herkesin kazandığı durum", "Rastgele sonuç", "En yüksek kâr", "John Nash'e aittir."),
    ("Sezgisel (heuristic) yöntem nedir?", "Optimumu garanti etmeyen ama pratik çözüm bulan yöntem", "Kesin optimum veren yöntem", "Yalnızca el hesabı", "Rastgele tahmin", "Büyük problemlerde hızlı sonuç verir."),
    ("Genetik algoritma neyden esinlenir?", "Doğal seçilim ve evrim", "Metal soğutma", "Karınca davranışı", "Atom yapısı", "Çaprazlama ve mutasyon kullanır."),
    ("Tavlama benzetimi (simulated annealing) neyden esinlenir?", "Metalin kontrollü soğutulmasından", "Doğal seçilimden", "Kuş sürülerinden", "Güneş sisteminden", "Sıcaklık parametresi zamanla düşer."),
    ("Tabu araştırmasında ne yapılır?", "Yakın zamanda ziyaret edilen çözümler yasaklanır", "Rastgele tüm çözümler denenir", "Sadece en iyi çözüme gidilir", "Kısıtlar silinir", "Hafıza kullanarak döngüden kaçınır."),
    ("Çok amaçlı optimizasyon nedir?", "Birden fazla çelişen amacı birlikte ele almak", "Tek amacı en büyüklemek", "Kısıtsız çözmek", "Tahmin yapmak", "Kâr artarken maliyet düşsün gibi."),
    ("Hedef programlama neyi minimize eder?", "Hedef değerlerden sapmaları", "Sadece maliyeti", "Sadece süreyi", "Kısıt sayısını", "Her hedef için istenen seviyeden sapma ölçülür."),
    ("Yöneylem araştırması hangi dönemde doğmuştur?", "II. Dünya Savaşı sırasında askeri problemlerde", "Sanayi Devrimi'nde", "1990'larda", "Bilgisayarın icadından önce 1800'lerde", "İngiltere'de radar ve konvoy planlamasıyla başlamıştır."),
    ("Boş (slack) değişken ne işe yarar?", "≤ kısıtını eşitliğe çevirmek için eklenir", "Amaç fonksiyonunu siler", "Maliyeti artırır", "Kısıt sayısını azaltır", "Kullanılmayan kaynak miktarını gösterir."),
    ("Karar değişkeni nedir?", "Modelde değerini belirlemeye çalıştığımız büyüklük", "Sabit sayı", "Rastgele hata", "Kısıt sağ tarafı", "Örneğin 'kaç adet üretilecek'."),
    ("Duyarlılık analizi neyi inceler?", "Parametre değişimlerinin optimal çözüme etkisini", "Rastgele sayıları", "Kuyruk uzunluğunu", "Stok miktarını", "'Ya şu değer değişirse?' sorusuna yanıt arar."),

    # ---------------- İSTATİSTİK VE OLASILIK ----------------
    ("Normal dağılımda ortalamanın ±1 standart sapma çevresinde yaklaşık yüzde kaç veri bulunur?", "%68", "%50", "%95", "%99.7", "Ampirik kural: 68-95-99.7."),
    ("Normal dağılımda ±2 standart sapma yaklaşık yüzde kaç veriyi kapsar?", "%95", "%68", "%75", "%50", "Ampirik kuralın ikinci adımı."),
    ("Normal dağılımda ±3 standart sapma yaklaşık yüzde kaç veriyi kapsar?", "%99.7", "%95", "%68", "%90", "Altı Sigma mantığının temelidir."),
    ("Merkezi limit teoremi ne der?", "Örneklem ortalamalarının dağılımı örnek büyüdükçe normale yaklaşır", "Her veri normaldir", "Varyans sıfırdır", "Ortalama her zaman medyandır", "Ana kütle dağılımından bağımsız olarak geçerlidir."),
    ("Varyans neye eşittir?", "Standart sapmanın karesine", "Ortalamanın yarısına", "Medyanın iki katına", "Aralığa", "σ² olarak gösterilir."),
    ("Medyan nedir?", "Sıralı verinin ortadaki değeri", "En sık görülen değer", "Aritmetik ortalama", "En büyük değer", "Veri küçükten büyüğe sıralanır."),
    ("Mod nedir?", "En sık tekrar eden değer", "Ortadaki değer", "Ortalama", "En küçük değer", "Frekansı en yüksek gözlemdir."),
    ("Poisson dağılımı neyi modeller?", "Belirli bir aralıkta olay sayısını", "İki olay arası süreyi", "Sürekli ölçümleri", "Tek denemenin sonucunu", "Örnek: saatte gelen müşteri sayısı."),
    ("Üstel dağılım neyi modeller?", "Olaylar arasındaki süreyi", "Başarı sayısını", "Kusur sayısını", "Hatalı oranı", "Poisson sürecinde olaylar arası süre üsteldir."),
    ("Binom dağılımı neyi modeller?", "n bağımsız denemede başarı sayısını", "Olaylar arası süreyi", "Sürekli ölçüyü", "Ortalama varyansı", "Başarı-başarısızlık denemeleri."),
    ("Tip I hata nedir?", "Doğru olan H0'ı reddetmek", "Yanlış olan H0'ı kabul etmek", "Örneklemi küçük seçmek", "Veriyi kaybetmek", "α ile gösterilir."),
    ("Tip II hata nedir?", "Yanlış olan H0'ı reddedememek", "Doğru H0'ı reddetmek", "Veriyi yanlış girmek", "Hipotez kurmamak", "β ile gösterilir."),
    ("p-değeri neyi ifade eder?", "H0 doğruysa gözlenen veya daha uç sonucun olasılığını", "H0'ın doğru olma olasılığını", "Hata oranını", "Örnek büyüklüğünü", "Küçük p-değeri H0'a karşı kanıttır."),
    ("Güven aralığı nedir?", "Parametrenin belirli güvenle içinde olması beklenen aralık", "Veri aralığı", "Hata oranı", "Tahmin hatası", "Örneğin %95 güven aralığı."),
    ("Korelasyon katsayısı hangi aralıktadır?", "−1 ile +1", "0 ile 100", "−100 ile 100", "0 ile 1 arası pozitif", "−1 tam negatif, +1 tam pozitif ilişkidir."),
    ("Regresyonda R² neyi gösterir?", "Bağımlı değişkenin değişkenliğinin açıklanan oranını", "Hata sayısını", "Eğimi", "Örnek sayısını", "0 ile 1 arasında bir değerdir."),
    ("ANOVA ne için kullanılır?", "İkiden fazla grubun ortalamasını karşılaştırmak için", "Tek ortalamayı test etmek için", "Zaman serisi tahmini için", "Kuyruk analizi için", "Varyans analizidir."),
    ("Ki-kare testi hangi tür veri için kullanılır?", "Kategorik veriler", "Sadece sürekli veriler", "Zaman serisi", "Yalnızca ağırlıklar", "Bağımsızlık ve uyum iyiliği testlerinde kullanılır."),
    ("t-testi ne zaman kullanılır?", "Küçük örneklemde ve σ bilinmediğinde ortalama testinde", "Kategorik verilerde", "Zaman serisinde", "Kuyruk modelinde", "Student t dağılımına dayanır."),
    ("Bayes teoremi neyi sağlar?", "Yeni bilgiyle koşullu olasılığı güncellemeyi", "Ortalamayı bulmayı", "Varyansı hesaplamayı", "Trendi tahmin etmeyi", "Önsel olasılıktan sonsal olasılığa geçilir."),
    ("A ve B bağımsız olaylarsa P(A ve B) neye eşittir?", "P(A) × P(B)", "P(A) + P(B)", "P(A) − P(B)", "P(A) / P(B)", "Bağımsızlıkta olasılıklar çarpılır."),
    ("Standart normal dağılımın ortalaması ve standart sapması nedir?", "0 ve 1", "1 ve 0", "0 ve 0", "1 ve 1", "Z dağılımıdır."),
    ("Z skoru neyi gösterir?", "Bir değerin ortalamadan kaç standart sapma uzakta olduğunu", "Ortalamanın kendisini", "Varyansı", "Örnek sayısını", "(x − μ) / σ"),
    ("Örneklem büyüklüğü artarsa standart hata nasıl değişir?", "Azalır", "Artar", "Değişmez", "Sıfır olur", "σ/√n formülüne bakın."),
    ("Varyasyon katsayısı nasıl hesaplanır?", "Standart sapma / ortalama", "Ortalama / standart sapma", "Varyans × ortalama", "Medyan − mod", "Göreli değişkenliği gösterir."),

    # ---------------- MÜHENDİSLİK EKONOMİSİ ----------------
    ("Paranın zaman değeri ne demektir?", "Bugünkü paranın gelecekteki aynı miktardan daha değerli olması", "Paranın her zaman aynı değerde olması", "Paranın enflasyondan etkilenmemesi", "Faizin olmaması", "Para yatırılıp getiri sağlayabilir."),
    ("Net Bugünkü Değer (NBD) pozitifse ne yapılır?", "Proje kabul edilebilir", "Proje reddedilir", "Karar verilemez", "Proje durdurulur", "Getirisi maliyetini aşar."),
    ("İç verim oranı (IRR) nedir?", "NBD'yi sıfır yapan iskonto oranı", "Enflasyon oranı", "Vergi oranı", "Amortisman oranı", "Projenin kendi getiri oranıdır."),
    ("Geri ödeme süresi neyi gösterir?", "Yatırımın geri kazanılma süresini", "Projenin toplam kârını", "Ürün ömrünü", "Faiz oranını", "Başlangıç yatırımı ne zaman çıkar."),
    ("MARR kısaltması neyi ifade eder?", "Kabul edilebilir minimum çekici getiri oranı", "Maksimum yıllık getiri", "Ortalama aylık kâr", "Makine amortisman oranı", "Yatırımcının aradığı en düşük getiri."),
    ("Amortisman nedir?", "Varlığın değerinin zamana yayılarak maliyete aktarılması", "Kredi faizi", "Vergi iadesi", "Stok değeri", "Değer kaybı muhasebeleştirilir."),
    ("Doğrusal amortismanda ne olur?", "Her yıl eşit tutarda amortisman ayrılır", "İlk yıl en çok ayrılır", "Hiç ayrılmaz", "Son yıl hepsi ayrılır", "(Maliyet − hurda değer) / ömür."),
    ("Bileşik faizde ne olur?", "Faiz, birikmiş faiz üzerinden de işler", "Faiz sadece anapara üzerinden işler", "Faiz sıfırdır", "Faiz sabittir ve eklenmez", "Faizin faizi kavramı vardır."),
    ("Fayda/maliyet oranı 1'den büyükse ne anlama gelir?", "Faydalar maliyetlerden büyüktür", "Maliyetler faydadan büyüktür", "Proje zarardadır", "Hiçbir şey ifade etmez", "B/C > 1 olumlu bir göstergedir."),
    ("Başabaş analizi neyi bulur?", "Gelirin toplam maliyete eşit olduğu üretim miktarını", "En yüksek kârı", "En düşük maliyeti", "Stok seviyesini", "Ne kâr ne zarar noktasıdır."),
    ("Hangisi sabit maliyet örneğidir?", "Fabrika kirası", "Hammadde", "Parça başı işçilik", "Ambalaj", "Üretim miktarından bağımsızdır."),
    ("Hangisi değişken maliyet örneğidir?", "Hammadde", "Fabrika kirası", "Yönetici maaşı", "Sigorta primi", "Üretimle birlikte artar."),
    ("Fırsat maliyeti nedir?", "Vazgeçilen en iyi alternatifin değeri", "Ödenen vergi", "Makine maliyeti", "Faiz geliri", "Seçim yaparken kaybedilen fırsattır."),
    ("Batık maliyet (sunk cost) nedir?", "Geri alınamayan geçmiş maliyet", "Gelecekteki maliyet", "Değişken maliyet", "Marjinal maliyet", "Yeni karar verirken dikkate alınmamalıdır."),
    ("Enflasyon nedir?", "Genel fiyat düzeyinde sürekli artış", "Fiyatların düşmesi", "Faizlerin düşmesi", "Üretimin artması", "Paranın satın alma gücü azalır."),
    ("Anüite nedir?", "Eşit aralıklarla yapılan eşit tutarlı ödemeler", "Tek seferlik ödeme", "Rastgele ödemeler", "Artan ödemeler", "Kira, taksit gibi düzenli ödemeler."),
    ("Marjinal maliyet nedir?", "Bir birim ek üretimin getirdiği ek maliyet", "Toplam sabit maliyet", "Ortalama maliyet", "Vergi", "Üretim bir birim artınca maliyetin değişimi."),
    ("İskonto oranı yükselirse NBD genellikle nasıl değişir?", "Düşer", "Artar", "Değişmez", "Sıfırlanır", "Gelecek nakit akışları daha az değerli olur."),
    ("Hurda değeri (salvage value) nedir?", "Varlığın ömrü sonundaki kalan değeri", "İlk alış fiyatı", "Yıllık amortisman", "Bakım maliyeti", "Ömrü bitince elde edilebilecek değer."),
    ("Nominal faiz ile reel faiz arasındaki fark neyi içerir?", "Enflasyonu", "Vergiyi", "Amortismanı", "Stok maliyetini", "Reel faiz ≈ nominal faiz − enflasyon."),

    # ---------------- İŞ ETÜDÜ VE ERGONOMİ ----------------
    ("İş etüdünün iki temel bileşeni hangisidir?", "Yöntem etüdü ve iş ölçümü", "Maliyet ve kalite", "Stok ve sipariş", "Tahmin ve planlama", "Hem yöntemi iyileştirir hem süreyi ölçer."),
    ("Bilimsel yönetimin babası olarak kabul edilen kişi kimdir?", "Frederick Taylor", "Henri Fayol", "Max Weber", "Henry Ford", "Zaman etüdü çalışmalarıyla tanınır."),
    ("Hareket etüdünün öncüleri kimlerdir?", "Frank ve Lillian Gilbreth", "Henry Ford ve Taylor", "Ohno ve Shingo", "Weber ve Fayol", "Therblig kavramını geliştirmişlerdir."),
    ("Therblig nedir?", "Temel hareket birimleri", "Bir kalite aracı", "Stok birimi", "Bakım yöntemi", "Gilbreth soyadının ters yazılışıdır."),
    ("Standart süre nasıl bulunur?", "Normal süre + paylar (toleranslar)", "Gözlenen süre × 2", "Ortalama süre − pay", "Maksimum süre", "Yorgunluk ve kişisel ihtiyaç payları eklenir."),
    ("Normal süre nasıl hesaplanır?", "Gözlenen süre × performans derecesi", "Gözlenen süre / 2", "Standart süre − pay", "Toplam süre + fire", "Çalışanın hızı normalize edilir."),
    ("İş örneklemesi (work sampling) nedir?", "Rastgele anlık gözlemlerle iş dağılımını belirleme", "Tüm günü saniye saniye izleme", "Ürün muayenesi", "Anket yapma", "İstatistiksel örnekleme kullanır."),
    ("Akış süreç şemasında hangi eylem sembolü yoktur?", "Pazarlama", "Operasyon", "Taşıma", "Bekleme", "Operasyon, taşıma, muayene, bekleme ve depolama vardır."),
    ("Ergonomi nedir?", "İnsan, makine ve çevre uyumunu inceleyen bilim", "Maliyet muhasebesi", "Kalite kontrolü", "Stok yönetimi", "İşi insana uydurmayı amaçlar."),
    ("RULA ve REBA yöntemleri neyi değerlendirir?", "Çalışma duruşunun kas-iskelet riskini", "Maliyeti", "Stok devrini", "Kalite hatasını", "Üst uzuv ve tüm vücut duruş analizleridir."),
    ("NIOSH denklemi ne için kullanılır?", "Güvenli yük kaldırma sınırını belirlemek için", "Stok hesaplamak için", "Maliyet bulmak için", "Kuyruk analizi için", "Elle taşıma işlerinde önerilen ağırlık sınırı."),
    ("Hawthorne etkisi nedir?", "Gözlenen çalışanların performansının değişmesi", "Makine hızının artması", "Stokun azalması", "Kalitenin düşmesi", "Elton Mayo çalışmalarıyla ilişkilidir."),
    ("İhtiyaçlar hiyerarşisini kim ortaya koymuştur?", "Abraham Maslow", "Herzberg", "McGregor", "Taylor", "Piramit şeklinde gösterilir."),
    ("Herzberg'in teorisi nedir?", "İki faktör (hijyen ve motivasyon) teorisi", "X ve Y teorisi", "İhtiyaçlar hiyerarşisi", "Beklenti teorisi", "Memnuniyet ve memnuniyetsizlik farklı faktörlerden gelir."),
    ("McGregor'un X ve Y teorisi neyi anlatır?", "Yöneticilerin çalışanlara bakış varsayımlarını", "Stok yöntemlerini", "Kalite araçlarını", "Maliyet tiplerini", "X: çalışan tembeldir, Y: çalışan motivedir."),
    ("Fitts yasası neyi ifade eder?", "Hedefe ulaşma süresinin mesafe ve hedef boyutuna bağlı olduğunu", "Stok yasasını", "Kuyruk uzunluğunu", "Kalite maliyetini", "Ergonomi ve insan-bilgisayar etkileşiminde kullanılır."),
    ("Gürültü hangi birimle ölçülür?", "Desibel (dB)", "Lüks (lux)", "Newton", "Watt", "Ses şiddeti birimidir."),
    ("Aydınlatma şiddeti hangi birimle ölçülür?", "Lüks (lux)", "Desibel", "Joule", "Amper", "Yüzeye düşen ışık miktarı."),
    ("Yöntem etüdünün amacı nedir?", "İşin yapılış yöntemini iyileştirmek", "Maaşları belirlemek", "Stok saymak", "Satış yapmak", "Daha kolay, hızlı ve ucuz yöntem bulunur."),
    ("Kas-iskelet sistemi rahatsızlıklarının önemli nedeni hangisidir?", "Tekrarlı hareketler ve kötü duruş", "Yüksek maaş", "Yeterli dinlenme", "İyi aydınlatma", "Ergonomik risk faktörleridir."),

    # ---------------- TESİS YERLEŞİMİ VE LOJİSTİK ----------------
    ("Ürün tipi yerleşimde makineler nasıl dizilir?", "Ürünün işlem sırasına göre", "Benzer makineler bir arada", "Rastgele", "Ürün sabit, makineler gelir", "Montaj hattı buna örnektir."),
    ("Süreç tipi (fonksiyonel) yerleşim nedir?", "Benzer işlevli makinelerin bir arada toplanması", "Montaj hattı kurmak", "Ürünü sabit tutmak", "Hücreler oluşturmak", "Atölye tipi üretimde kullanılır."),
    ("Sabit konumlu yerleşim hangi ürünler için uygundur?", "Gemi, köprü gibi büyük ürünler", "Küçük elektronik parçalar", "Gıda ürünleri", "Kâğıt ürünler", "Ürün sabit kalır, kaynaklar ürüne gider."),
    ("Sistematik Yerleşim Planlaması (SLP) kime aittir?", "Richard Muther", "Frederick Taylor", "Taiichi Ohno", "George Dantzig", "İlişki diyagramı kullanır."),
    ("Hat dengeleme neyi amaçlar?", "İşleri istasyonlara dengeli dağıtarak boşta bekleme azaltmayı", "Stoku artırmayı", "Kalite kontrolü yapmayı", "Fiyat belirlemeyi", "İstasyon süreleri birbirine yaklaştırılır."),
    ("Çevrim süresi (cycle time) nedir?", "Hattan iki ürün çıkışı arasındaki süre", "Toplam çalışma yılı", "Bakım aralığı", "Tedarik süresi", "Hattın ritmini belirler."),
    ("Darboğaz (bottleneck) nedir?", "Sistem kapasitesini belirleyen en yavaş istasyon", "En hızlı makine", "Boş depo", "Yönetim kurulu", "Tüm hattın çıktısını sınırlar."),
    ("AGV nedir?", "Otomatik yönlendirmeli araç", "Yıllık gelir tablosu", "Üretim yöntemi", "Kalite kartı", "Fabrikada malzeme taşıyan robot araç."),
    ("WMS ne anlama gelir?", "Depo yönetim sistemi", "Çalışma ölçüm standardı", "Üretim planı", "Satış modülü", "Depo operasyonlarını yazılımla yönetir."),
    ("RFID nedir?", "Radyo frekansıyla otomatik tanımlama teknolojisi", "Barkod yazıcısı", "Kalite grafiği", "Maliyet yöntemi", "Etiket temassız okunur."),
    ("Tesis yeri seçiminde ağırlık merkezi yöntemi neyi bulur?", "Taşıma maliyetini minimize eden konumu", "Maksimum kârı", "En yüksek kiralı yeri", "En az işçiyi", "Koordinat ve talep ağırlıklarıyla hesaplanır."),
    ("Faktör derecelendirme yöntemi nedir?", "Ağırlıklandırılmış kriterlerle yer seçimi", "Stok yöntemi", "Kuyruk analizi", "Simülasyon", "Niteliksel ve niceliksel kriterler puanlanır."),
    ("3PL ne demektir?", "Üçüncü parti lojistik", "Üç parçalı üretim", "Üç aşamalı planlama", "Üç yıllık plan", "Lojistik hizmetini dış firmadan almak."),
    ("Kapasite kullanım oranı nasıl hesaplanır?", "Gerçek üretim / tasarım kapasitesi", "Tasarım kapasitesi / gerçek üretim", "Toplam maliyet / satış", "Stok / talep", "Kapasitenin ne kadarının kullanıldığını gösterir."),
    ("Verimlilik nedir?", "Çıktı / girdi", "Girdi / çıktı", "Maliyet − gelir", "Satış / stok", "Kaynakların ne kadar iyi kullanıldığı."),
    ("Incoterms neyi düzenler?", "Uluslararası ticarette teslim şartlarını", "Maaş sistemlerini", "Üretim yöntemlerini", "Kalite standartlarını", "Alıcı ve satıcının sorumluluklarını belirler."),
    ("Hücresel yerleşimde hangi teknoloji temel alınır?", "Grup teknolojisi", "Kuyruk teorisi", "Simülasyon", "Oyun teorisi", "Benzer parçalar aileler halinde işlenir."),
    ("Malzeme taşıma ilkelerinden biri hangisidir?", "Taşıma mesafesini ve sayısını azaltmak", "Mümkün olduğunca uzun taşımak", "Taşımayı artırmak", "Rastgele taşımak", "Taşıma değer katmayan bir faaliyettir."),
    ("Ters lojistik nedir?", "Ürünlerin müşteriden geri dönüşüm veya iade amacıyla geri akışı", "Üretimin tersine çevrilmesi", "Stok azaltma", "Siparişin iptali", "İade, onarım ve geri kazanım süreçleridir."),
    ("Depo yönetiminde 'FIFO' ne demektir?", "İlk giren ilk çıkar", "Son giren ilk çıkar", "En değerli ilk çıkar", "Rastgele çıkar", "Raf ömrü olan ürünler için önemlidir."),

    # ---------------- PROJE YÖNETİMİ ----------------
    ("CPM'de kritik yol nedir?", "Projedeki en uzun faaliyet yolu", "En kısa yol", "En ucuz yol", "En fazla kaynak kullanan yol", "Projenin en kısa bitiş süresini belirler."),
    ("Kritik yoldaki faaliyetlerin bolluğu (slack) nedir?", "Sıfırdır", "Pozitiftir", "Negatif olamaz, çok yüksektir", "Rastgeledir", "Gecikme tüm projeyi geciktirir."),
    ("Gantt şeması neyi gösterir?", "Faaliyetleri zaman çizelgesi üzerinde", "Stok hareketini", "Maliyet dağılımını", "Kalite sonuçlarını", "Henry Gantt'a aittir."),
    ("PERT'te beklenen süre nasıl hesaplanır?", "(a + 4m + b) / 6", "(a + m + b) / 3", "(a + b) / 2", "(a × m × b)", "a iyimser, m olası, b kötümser süredir."),
    ("PERT'te bir faaliyetin varyansı nasıl hesaplanır?", "((b − a) / 6)²", "(b − a) / 2", "(a + b) / 6", "(m − a)²", "Kötümser ile iyimser süre farkının altıda biri, karesi."),
    ("İş kırılım yapısı (WBS) nedir?", "Projenin hiyerarşik alt işlere bölünmesi", "Maliyet tablosu", "Risk listesi", "Çalışan listesi", "Kapsamı yönetilebilir parçalara ayırır."),
    ("Proje süresini kısaltma (crashing) nedir?", "Ek maliyetle faaliyet sürelerini kısaltmak", "Projeyi iptal etmek", "Kapsamı genişletmek", "Faaliyetleri uzatmak", "Önce kritik yoldaki en ucuz faaliyet kısaltılır."),
    ("Kazanılmış değer yönetimi (EVM) neyi ölçer?", "Proje maliyet ve zaman performansını", "Çalışan memnuniyetini", "Stok seviyesini", "Satış gelirini", "Planlanan, gerçekleşen ve kazanılan değeri karşılaştırır."),
    ("Proje yönetiminin üçlü kısıtı nedir?", "Kapsam, zaman ve maliyet", "Kalite, hız, fiyat", "İnsan, makine, para", "Risk, kâr, vergi", "Biri değişirse diğerleri etkilenir."),
    ("Kilometre taşı (milestone) nedir?", "Projede önemli bir aşamanın tamamlandığı nokta", "Bir işçi ödülü", "Bir maliyet kalemi", "Bir makine tipi", "Süresi sıfır olan önemli olaydır."),
    ("PMBOK nedir?", "PMI'ın proje yönetimi bilgi birikimi rehberi", "Bir kalite standardı", "Bir üretim sistemi", "Bir yazılım dili", "Project Management Body of Knowledge."),
    ("Paydaş (stakeholder) kimdir?", "Projeden etkilenen veya projeyi etkileyen kişi/kurum", "Sadece proje yöneticisi", "Sadece tedarikçi", "Sadece müşteri", "Çıkar sahibi taraflardır."),
    ("CPM'de erken başlama zamanları nasıl bulunur?", "İleri geçişle", "Geri geçişle", "Rastgele", "Ortalamayla", "Başlangıçtan sona doğru hesaplanır."),
    ("CPM'de geç bitiş zamanları nasıl bulunur?", "Geri geçişle", "İleri geçişle", "Tahminle", "Ortalamayla", "Sondan başa doğru hesaplanır."),
    ("Risk yönetiminin doğru sırası hangisidir?", "Belirle, analiz et, yanıt planla, izle", "İzle, sil, gizle, unut", "Sat, üret, ölç, kapat", "Tahmin et, ceza ver, bitir", "Riskler önce belirlenir."),

    # ---------------- TAHMİN, SİMÜLASYON, KUYRUK ----------------
    ("Hareketli ortalama yöntemi neyi yapar?", "Son n dönemin ortalamasını alır", "Tüm veriyi toplar", "Sadece son veriyi kullanır", "Rastgele tahmin eder", "Dalgalanmaları yumuşatır."),
    ("Üstel düzeltme yönteminde ne olur?", "Son gözlemlere daha fazla ağırlık verilir", "Tüm gözlemler eşit ağırlıklıdır", "Eski veriler daha önemlidir", "Veri kullanılmaz", "Ağırlıklar geriye gittikçe üstel azalır."),
    ("MAD neyi ifade eder?", "Ortalama mutlak sapma", "Maksimum ağırlıklı değer", "Makine arıza düzeyi", "Medyan ağırlık dağılımı", "Tahmin hatası ölçüsüdür."),
    ("Mevsimsellik nedir?", "Düzenli aralıklarla tekrarlayan dönemsel dalgalanma", "Uzun vadeli artış", "Rastgele hata", "Tek seferlik olay", "Yaz-kış satış farkı gibi."),
    ("Delphi yöntemi nedir?", "Uzmanların tekrarlı anketlerle fikir birliğine varması", "Matematiksel model", "Zaman serisi", "Stok yöntemi", "Nitel tahmin tekniğidir."),
    ("MAPE nedir?", "Ortalama mutlak yüzde hata", "Maksimum ağırlıklı değer", "Maliyet analiz oranı", "Makine arıza periyodu", "Tahmin doğruluğunu yüzde olarak verir."),
    ("Monte Carlo simülasyonu nedir?", "Rastgele örneklemeyle belirsizliği modelleme", "Kesin formülle çözme", "Kuyruk formülü", "Doğrusal program", "Çok sayıda rastgele deneme yapılır."),
    ("Kesikli olay simülasyonunda sistem durumu ne zaman değişir?", "Yalnızca olay anlarında", "Sürekli", "Hiç değişmez", "Her saniye", "Müşteri varışı, hizmet bitişi gibi olaylar."),
    ("Little yasası nedir?", "L = λ × W", "L = λ / W", "L = W − λ", "L = λ + W", "Ortalama sistemdeki sayı = varış hızı × ortalama bekleme."),
    ("M/M/1 kuyruk modelinde ne vardır?", "Poisson varış, üstel hizmet, tek sunucu", "Sabit varış, sabit hizmet, çok sunucu", "Rastgele varış, tek sunucu, sınırsız", "İki sunucu", "Kendall notasyonuyla gösterilir."),
    ("Kuyruğun kararlı olması için ne gerekir?", "Kullanım oranı ρ < 1", "ρ > 1", "ρ = 2", "ρ = 0 olmalı", "Varış hızı hizmet hızından küçük olmalıdır."),
    ("Kuyruk sisteminde kullanım oranı (ρ) nedir?", "λ / μ", "μ / λ", "λ × μ", "λ − μ", "Varış hızının hizmet hızına oranıdır."),
    ("Kuyruk teorisinin kurucusu kimdir?", "A. K. Erlang", "Henry Gantt", "Walter Shewhart", "Vilfredo Pareto", "Telefon santrali çalışmalarıyla başlamıştır."),
    ("Simülasyonun avantajı nedir?", "Gerçek sistemi bozmadan senaryoları denemek", "Her zaman kesin sonuç vermek", "Maliyetsiz olmak", "Veri gerektirmemek", "Risksiz deneme ortamı sağlar."),
    ("Simülasyon modelinin doğrulanması (validation) neyi kontrol eder?", "Modelin gerçek sistemi doğru temsil edip etmediğini", "Kodun hızını", "Ekran rengini", "Dosya boyutunu", "Gerçeğe uygunluk testidir."),
    ("Markov zincirinde gelecek neye bağlıdır?", "Yalnızca mevcut duruma", "Tüm geçmişe", "Rastgele bir sayıya", "Hiçbir şeye", "Hafızasızlık özelliği vardır."),
    ("Zaman serisinde trend nedir?", "Uzun vadeli artış veya azalış eğilimi", "Rastgele hata", "Mevsimsel dalga", "Tek seferlik şok", "Yönlü uzun dönem hareketidir."),
    ("Tahmin yönteminde regresyon neye dayanır?", "Bağımlı ve bağımsız değişken ilişkisine", "Rastgele sayıya", "Sadece son veriye", "Sadece uzman görüşüne", "Bir değişkenle diğerini açıklar."),
    ("FIFO ve LIFO disiplinleri nerede kullanılır?", "Kuyruk ve stok sıralama kurallarında", "Maaş hesabında", "Vergi hesabında", "Kalite kartlarında", "Sıranın nasıl belirlendiğini gösterir."),
    ("Simülasyonda 'ısınma (warm-up) dönemi' neden kullanılır?", "Başlangıç etkisini sonuçlardan çıkarmak için", "Ekranı ısıtmak için", "Veriyi silmek için", "Hızı artırmak için", "Sistem kararlı hale gelene kadar beklenir."),

    # ---------------- TEDARİK ZİNCİRİ VE GENEL ----------------
    ("Kırbaç (bullwhip) etkisi nedir?", "Talep dalgalanmasının tedarik zincirinde yukarı doğru büyümesi", "Stokların azalması", "Fiyatların düşmesi", "Kalitenin artması", "Perakendeciden üreticiye doğru değişkenlik büyür."),
    ("Tedarik zinciri yönetimi neyi koordine eder?", "Tedarikçiden müşteriye ürün, bilgi ve para akışını", "Sadece üretimi", "Sadece satışı", "Sadece muhasebeyi", "Uçtan uca bir bakış gerektirir."),
    ("SCOR modeli nedir?", "Tedarik zinciri operasyon referans modeli", "Bir kalite aracı", "Yalın aracı", "Zaman ölçüm yöntemi", "Plan, tedarik, üretim, teslimat, iade süreçlerini tanımlar."),
    ("VMI (tedarikçi yönetimli stok) nedir?", "Tedarikçinin müşterinin stoğunu yönetmesi", "Müşterinin tedarikçiyi yönetmesi", "Stok saklamama", "Fiyat sabitleme", "Tedarikçi stoktan sorumludur."),
    ("Dış kaynak kullanımı (outsourcing) nedir?", "Bir faaliyetin dış firmaya yaptırılması", "Personel eğitimi", "Stok biriktirme", "Üretimi durdurma", "Çekirdek olmayan işler dışarıya verilir."),
    ("Endüstri 4.0'ın temel bileşenlerinden biri hangisidir?", "Nesnelerin interneti (IoT)", "Buhar makinesi", "Elle üretim", "Mekanik dokuma tezgâhı", "Siber-fiziksel sistemler ve bağlantılı makineler."),
    ("Dijital ikiz nedir?", "Fiziksel bir sistemin sanal kopyası", "İki özdeş makine", "Çift vardiya", "Yedek depo", "Gerçek zamanlı verilerle sanal modeli günceller."),
    ("ERP sistemi nedir?", "Kurumsal kaynak planlama yazılımı", "Bir üretim makinesi", "Bir kalite grafiği", "Bir tahmin yöntemi", "Finans, üretim, satın alma gibi modülleri bütünleştirir."),
    ("Sürdürülebilirliğin üç ayağı hangisidir?", "Ekonomik, çevresel ve sosyal", "Hız, kalite, fiyat", "Para, zaman, insan", "Üretim, satış, ihracat", "Triple bottom line olarak da bilinir."),
    ("Hareketli montaj hattını yaygınlaştıran kişi kimdir?", "Henry Ford", "Frederick Taylor", "Taiichi Ohno", "W. E. Deming", "Model T üretiminde kullanmıştır."),
    ("Yönetimin fonksiyonlarını (planlama, örgütleme, yöneltme, koordinasyon, kontrol) tanımlayan kimdir?", "Henri Fayol", "Max Weber", "Abraham Maslow", "Walter Shewhart", "Klasik yönetim kuramcısı."),
    ("W. Edwards Deming hangi alanla özdeşleşmiştir?", "Kalite yönetimi ve PDCA", "Hareket etüdü", "Oyun teorisi", "Stok kontrolü", "14 ilke ve Deming Ödülü."),
    ("Pareto ilkesi (80/20) ne söyler?", "Sonuçların çoğunun az sayıda nedenden kaynaklandığını", "Her şey eşit dağılır", "Rastgele sonuç olur", "Nedenler sonuçlardan fazladır", "Yaklaşık %80 sonuç %20 nedenden gelir."),
    ("Endüstri mühendisliği neyi optimize etmeyi hedefler?", "İnsan, makine, malzeme, bilgi ve enerji sistemlerinin bütününü", "Sadece makineleri", "Sadece bilgisayarları", "Sadece satış rakamlarını", "Bütünsel sistem yaklaşımı vardır."),
    ("Michael Porter'ın ünlü modeli hangisidir?", "Beş güç analizi", "5S", "SMED", "DMAIC", "Sektör rekabet yapısını analiz eder."),
    ("Dengeli Performans Karnesi (Balanced Scorecard) kime aittir?", "Kaplan ve Norton", "Taylor ve Fayol", "Ohno ve Toyoda", "Dantzig ve Bellman", "Finansal olmayan göstergeleri de içerir."),
    ("KPI nedir?", "Temel performans göstergesi", "Kalite planı", "Kapasite planlama indeksi", "Kritik proje işlemi", "Hedeflere ulaşma düzeyini ölçer."),
    ("Kıyaslama (benchmarking) nedir?", "En iyi uygulamalarla karşılaştırarak performansı iyileştirmek", "Fiyat kırmak", "Stok artırmak", "Rakibi kopyalamak", "Sektör liderleriyle kıyaslanır."),
    ("Rekabet üstünlüğü sağlayan bir unsur hangisidir?", "Maliyet liderliği veya farklılaşma", "Rakibi görmezden gelmek", "Kaliteyi düşürmek", "Müşteriyi azaltmak", "Porter'ın genel stratejileri."),
    ("Siber-fiziksel sistem nedir?", "Fiziksel süreçlerle yazılımın iç içe çalıştığı sistem", "Sadece yazılım", "Sadece makine", "Sadece sensör", "Endüstri 4.0'ın temelidir."),
    ("Yapay zekâ üretimde en çok hangi amaçla kullanılır?", "Tahmine dayalı bakım ve kalite tespiti", "Çalışanları azaltmak tek amaçtır", "Stok tutmamak", "Fiyatı sabit tutmak", "Verilerden örüntü öğrenir."),

    # ---------------- ÇİZELGELEME, BAKIM, İŞ GÜVENLİĞİ ----------------
    ("SPT çizelgeleme kuralı ne yapar?", "En kısa işlem süreli işi öne alır", "En uzun işi öne alır", "Rastgele seçer", "Son geleni seçer", "Ortalama akış süresini minimize eder."),
    ("EDD çizelgeleme kuralı neye göre sıralar?", "En erken teslim tarihine", "En kısa süreye", "En uzun süreye", "Maliyete", "Gecikmeyi azaltmayı hedefler."),
    ("Johnson kuralı hangi problem için kullanılır?", "İki makineli akış tipi çizelgeleme", "Stok sipariş", "Kuyruk analizi", "Ağ akışı", "Toplam tamamlanma süresini (makespan) azaltır."),
    ("Makespan nedir?", "Tüm işlerin tamamlanma süresi", "Bir işin işlem süresi", "Ortalama gecikme", "Bekleme süresi", "Çizelgenin toplam uzunluğudur."),
    ("Önleyici bakım nedir?", "Arıza olmadan önce yapılan planlı bakım", "Arıza sonrası onarım", "Makine satışı", "Operatör eğitimi", "Arızaları önlemek için planlanır."),
    ("MTBF neyi gösterir?", "Arızalar arası ortalama süreyi", "Ortalama onarım süresini", "Maliyet toplamını", "Makine fiyatını", "Güvenilirliğin ölçüsüdür."),
    ("MTTR neyi gösterir?", "Ortalama onarım süresini", "Arızalar arası süreyi", "Üretim hızını", "Stok devrini", "Arıza sonrası geri dönüş süresi."),
    ("Kullanılabilirlik (availability) nasıl hesaplanır?", "MTBF / (MTBF + MTTR)", "MTTR / MTBF", "MTBF × MTTR", "MTBF − MTTR", "Makinenin çalışır durumda olma oranı."),
    ("Banyo küveti eğrisi neyi gösterir?", "Arıza oranının ömür boyunca değişimini", "Stok devrini", "Kâr dağılımını", "Kuyruk uzunluğunu", "Erken arıza, yararlı ömür, aşınma dönemleri vardır."),
    ("Risk değerlendirmesi nedir?", "Tehlikeleri belirleyip risk seviyesini ölçme", "Sigorta yaptırma", "Üretimi durdurma", "Maliyeti hesaplama", "İş sağlığı ve güvenliğinin temelidir."),
    ("KKD ne demektir?", "Kişisel koruyucu donanım", "Kalite kontrol departmanı", "Kritik karar düzeyi", "Kapasite kullanım derecesi", "Baret, eldiven, gözlük gibi."),
    ("İş sağlığı ve güvenliğinde hiyerarşik önlem sırasının en etkili adımı nedir?", "Tehlikeyi ortadan kaldırmak", "KKD kullanmak", "Uyarı levhası asmak", "Eğitim vermek", "Kaynağında yok etmek en etkilidir."),
]

questions_pool = [
    {"q": q, "options": [c, a, b, d], "correct": 0, "hint": h}
    for (q, c, a, b, d, h) in _RAW
]


# ----------------------------- RENKLER --------------------------------
NAVY = "#050b2e"
NAVY2 = "#0a1544"
BLUE = "#1d3fa8"
GOLD = "#f2b632"
GOLD2 = "#c9a54a"
ORANGE = "#ff8a1f"
GREEN = "#1fa64a"
RED = "#e04040"
TEXT = "#f4f6ff"

# ----------------------------- OYUN SABİTLERİ --------------------------
GY = 470             # zemin (mantıksal koordinat, yükseklik 540 kabul edilir)
DS = 0.8             # dart ölçeği
GRAV = 0.22          # yerçekimi (küçült = daha kolay)
V0, V1 = 10, 14      # hız = V0 + güç * V1
POWER_SPEED = 0.014  # güç barı hızı (küçült = daha kolay)
HIT_R = 66           # hedef isabet yarıçapı

GAME_TIME = 300      # oyun süresi (saniye) -> 5 dakika
QUESTIONS_PER_ROUND = 5
WIN_SCORE = 300      # oyun sonunda "TEBRİKLER" ekranı için gereken puan

# Gerçek dart puanlaması: merkezden uzaklığa (dikey) göre halka puanları
# (en fazla uzaklık, puan, isim)
RING_SCORES = [
    (6, 50, "BULLSEYE (tam orta)"),
    (14, 25, "Dış bull"),
    (27, 20, "Yeşil halka"),
    (38, 15, "Krem halka"),
    (52, 10, "Kırmızı halka"),
    (62, 5, "Dış krem halka"),
    (9999, 1, "Kenar"),
]

SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen_questions.json")


def ring_points(dy):
    d = abs(dy)
    for lim, pts, name in RING_SCORES:
        if d <= lim:
            return pts, name
    return 1, "Kenar"


def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(seen):
    try:
        with open(SEEN_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(seen), f, ensure_ascii=False)
    except Exception:
        pass


def hexrgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def lerp(c1, c2, t):
    a, b = hexrgb(c1), hexrgb(c2)
    t = max(0, min(1, t))
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad(t, stops):
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0 + 1e-9))
    return stops[-1][1]


def rrect(c, x1, y1, x2, y2, r, **kw):
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
           x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return c.create_polygon(pts, smooth=True, **kw)


def radial_bg(c, W, H, outer, inner, cx=0.5, cy=0.5, steps=34, tags="bg"):
    c.create_rectangle(0, 0, W, H, fill=outer, outline="", tags=tags)
    for i in range(1, steps):
        t = i / (steps - 1)
        rx = W * 0.75 * (1 - t) + 10
        ry = H * 0.85 * (1 - t) + 10
        c.create_oval(W * cx - rx, H * cy - ry, W * cx + rx, H * cy + ry,
                      fill=lerp(outer, inner, t ** 1.4), outline="", tags=tags)


def lattice(c, W, H, color, gap=64, tags="bg"):
    for x in range(-H, W + H, gap):
        c.create_line(x, 0, x + H, H, fill=color, tags=tags)
        c.create_line(x + H, 0, x, H, fill=color, tags=tags)


def hearts_text(lives, total=5):
    return "".join("♥" if i < lives else "♡" for i in range(total))


class DartGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Endüstri Mühendisliği - Dart Challenge")
        self.root.configure(bg=NAVY)
        self.root.geometry("1280x720")
        self.fullscreen = True
        self.root.attributes("-fullscreen", True)

        fams = set(tkfont.families())

        def pick(cands):
            for f in cands:
                if f in fams:
                    return f
            return "Helvetica"

        self.disp = pick(["Bahnschrift", "Segoe UI Black", "Montserrat", "Poppins",
                          "Avenir Next", "Trebuchet MS", "DejaVu Sans"])
        self.body = pick(["Segoe UI", "Bahnschrift", "Avenir Next", "Helvetica Neue",
                          "DejaVu Sans"])
        self.mono = pick(["Bahnschrift", "Consolas", "Menlo", "DejaVu Sans Mono"])

        self.W = self.H = 0
        self.k = 1.0
        self.Wl = 960
        self.frame = 0
        self.mx = self.my = -1
        self.buttons = []
        self.fireflies = []
        self.session_data = []
        self.session_counter = 1
        self.ban_until = 0
        self.timer_job = None
        self.dialog_open = False
        self.target_x = 820
        self.deck = []

        self.canvas = tk.Canvas(self.root, bg=NAVY, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)

        self.qc = tk.Canvas(self.root, bg=NAVY, highlightthickness=0, bd=0)
        self.qc.bind("<Configure>", lambda e: self.draw_question_screen())

        self.new_game_state()
        self.root.bind("<Up>", self.angle_up)
        self.root.bind("<Down>", self.angle_down)
        self.root.bind("<space>", self.shoot_arrow)
        self.root.bind("<Key>", self.on_key)
        self.game_loop()
        self.start_timer()

    # ------------------------------------------------------- yardımcılar
    def fd(self, size, weight="bold"):
        return (self.disp, max(7, int(size)), weight)

    def fb(self, size, weight="normal"):
        return (self.body, max(7, int(size)), weight)

    def s(self, v):
        return max(7, int(v * self.k))

    def P(self, *pts):
        return [v * self.k for v in pts]

    def build_deck(self):
        """Hiç sorulmamış sorular öne alınır; her oyunda/etapta farklı sorular gelir."""
        seen = load_seen()
        unseen = [q for q in questions_pool if q["q"] not in seen]
        if not unseen:                      # hepsi sorulduysa baştan başla
            seen = set()
            save_seen(seen)
            unseen = list(questions_pool)
        old = [q for q in questions_pool if q["q"] in seen]
        random.shuffle(unseen)
        random.shuffle(old)
        return unseen + old

    def new_game_state(self):
        self.score = 0
        self.time_left = GAME_TIME
        self.is_paused = False
        self.lives = 5
        self.angle = 14.0
        self.state = "aim"      # aim | charge | fly | stuck
        self.power = 0.0
        self.power_dir = 1
        self.dart = {}
        self.stuck_timer = 0
        self.target_y = 250
        self.target_speed = 2.2
        self.consecutive_first_try_correct = 0
        self.consecutive_misses = 0
        self.game_active = True
        self.question_active = False
        self.current_round_correct = 0
        self.current_round_wrong = 0
        self.questions_asked_in_round = 0
        self.round_results = []
        self.deck = self.build_deck()
        self.current_q_idx = 0
        self.has_given_hint = False
        self.hit_points = 0
        self.hit_name = ""

    # ------------------------------------------------------------ girdi
    def on_motion(self, e):
        self.mx, self.my = e.x, e.y

    def on_click(self, e):
        for x1, y1, x2, y2, cmd in reversed(self.buttons):
            if x1 <= e.x <= x2 and y1 <= e.y <= y2:
                cmd()
                break

    def on_key(self, e):
        ks = e.keysym.lower()
        if ks == "escape" or ks == "f11":
            self.fullscreen = not self.fullscreen
            self.root.attributes("-fullscreen", self.fullscreen)
        elif ks == "p":
            self.toggle_pause()
        elif self.question_active and ks in ("a", "b", "c", "d"):
            self.check_answer("abcd".index(ks))

    def can_aim(self):
        return (self.game_active and not self.is_paused and not self.question_active
                and self.state in ("aim", "charge"))

    def angle_up(self, e=None):
        if self.can_aim() and self.angle < 45:
            self.angle += 1.0

    def angle_down(self, e=None):
        if self.can_aim() and self.angle > -30:
            self.angle -= 1.0

    def sway(self):
        return math.sin(self.frame * 0.08) * 1.2

    # --------------------------------------------------------- atış
    def pose(self):
        """Okçunun kol/el/dart ucu konumu (mantıksal koordinat)."""
        sw = self.sway() if self.state in ("aim", "charge") else 0
        a = math.radians(self.angle + sw)
        pull = self.power * 16 if self.state == "charge" else 0
        L = 50 - pull
        sx, sy = 88, 346
        hx, hy = sx + L * math.cos(a), sy - L * math.sin(a)
        tx, ty = hx + 36 * DS * math.cos(a), hy - 36 * DS * math.sin(a)
        return a, (sx, sy), (hx, hy), (tx, ty)

    def shoot_arrow(self, e=None):
        if time.time() < self.ban_until:
            rem = int(self.ban_until - time.time())
            self.dialog("Ceza süresi", f"Can haklarınız bitti!\n{rem // 60} dakika {rem % 60} saniye sonra tekrar deneyin.",
                        RED, "⏳")
            return
        if not self.game_active or self.is_paused or self.question_active:
            return
        if self.state == "aim":
            self.state = "charge"
            self.power = 0.0
            self.power_dir = 1
        elif self.state == "charge":
            a, _, _, (x, y) = self.pose()
            a += math.radians(random.uniform(-0.4, 0.4))
            v = V0 + self.power * V1
            self.dart = {"x": x, "y": y, "vx": v * math.cos(a), "vy": -v * math.sin(a)}
            self.state = "fly"

    def predict(self, power):
        a, _, _, (x, y) = self.pose()
        v = V0 + power * V1
        vx, vy = v * math.cos(a), -v * math.sin(a)
        pts = []
        for _ in range(220):
            vy += GRAV
            x += vx
            y += vy
            pts.append((x, y))
            if x > self.target_x or y > GY:
                break
        return pts

    # -------------------------------------------------- oyun döngüsü
    def game_loop(self):
        try:
            self.frame += 1
            W, H = self.canvas.winfo_width(), self.canvas.winfo_height()
            if W > 50 and H > 50 and (W, H) != (self.W, self.H):
                self.on_resize(W, H)

            if self.game_active and not self.is_paused and not self.question_active:
                if self.state != "stuck":
                    self.target_y += self.target_speed
                    if self.target_y < 150 or self.target_y > 395:
                        self.target_speed *= -1

                if self.state == "charge":
                    self.power += POWER_SPEED * self.power_dir
                    if self.power >= 1:
                        self.power, self.power_dir = 1, -1
                    elif self.power <= 0:
                        self.power, self.power_dir = 0, 1

                elif self.state == "fly":
                    d = self.dart
                    d["vy"] += GRAV
                    d["x"] += d["vx"]
                    d["y"] += d["vy"]
                    if (self.target_x - 6 <= d["x"] <= self.target_x + 30
                            and abs(d["y"] - self.target_y) <= HIT_R):
                        self.on_hit(d["y"])
                    elif d["x"] > self.target_x + 30 or d["y"] > GY or d["y"] < 0:
                        self.on_miss()

                elif self.state == "stuck":
                    self.stuck_timer -= 1
                    if self.stuck_timer <= 0:
                        self.after_hit()

            if not self.question_active and self.W > 50:
                self.draw_scene()
            self.root.after(16, self.game_loop)
        except tk.TclError:
            pass

    def on_resize(self, W, H):
        self.W, self.H = W, H
        self.k = H / 540.0
        self.Wl = W / self.k
        self.target_x = self.Wl - 140
        rnd = random.Random(3)
        self.fireflies = [(rnd.random(), 0.45 + rnd.random() * 0.4, rnd.random() * 6.28)
                          for _ in range(22)]
        self.draw_forest()

    def on_hit(self, y):
        d = self.dart
        d["x"] = self.target_x - 4
        d["dy"] = y - self.target_y
        # Gerçek dart puanı: dartın merkeze uzaklığına göre
        self.hit_points, self.hit_name = ring_points(d["dy"])
        self.state = "stuck"
        self.stuck_timer = 45

    def after_hit(self):
        self.score += self.hit_points
        self.consecutive_misses = 0
        pts = self.hit_points
        icon = "🔴" if pts >= 50 else "🎯"
        title = "BULLSEYE!" if pts >= 50 else "İsabet!"
        self.state = "aim"
        self.dialog(title, f"{self.hit_name}\n+{pts} puan", GOLD, icon, "SORUYA GEÇ")
        self.switch_to_question_mode()

    def on_miss(self):
        # Iskalamak puan kazandırmaz ama oyunu bitirmez
        self.state = "aim"
        self.dialog("Iskaladın!", "Bu atıştan puan gelmedi.\nBir daha dene, süre akıyor!", ORANGE, "💨", "DEVAM")

    # ---------------------------------------------------- orman arka planı
    def pine(self, cx, base, h, w, dark, light, trunk="#3b2616"):
        c = self.canvas
        c.create_rectangle(cx - w * 0.06, base - h * 0.14, cx + w * 0.06, base,
                           fill=trunk, outline="", tags="bg")
        for i in range(4):
            yb = base - h * 0.10 - i * h * 0.2
            yt = yb - h * 0.34
            hw = w * 0.5 * (1 - i * 0.18)
            c.create_polygon(cx, yt, cx + hw, yb, cx - hw, yb, fill=dark, outline="", tags="bg")
            c.create_polygon(cx, yt, cx + hw, yb, cx, yb, fill=light, outline="", tags="bg")

    def draw_forest(self):
        c, W, H = self.canvas, self.W, self.H
        c.delete("bg")
        rnd = random.Random(5)
        stops = [(0, "#0d2438"), (0.45, "#2a6a78"), (0.8, "#e8b673"), (1, "#f6d9a0")]
        n = 56
        for i in range(n):
            c.create_rectangle(0, H * 0.78 * i / n, W, H * 0.78 * (i + 1) / n + 2,
                               fill=grad(i / (n - 1), stops), outline="", tags="bg")
        # güneş
        sx, sy = W * 0.74, H * 0.50
        for i in range(9):
            r = H * (0.30 - i * 0.03)
            c.create_oval(sx - r, sy - r, sx + r, sy + r,
                          fill=lerp("#eec37f", "#fff6d6", i / 8), outline="", tags="bg")
        # dağlar
        for base, col, amp in ((0.70, "#5a7a92", 0.16), (0.72, "#3f6272", 0.12)):
            pts = [0, H * base]
            steps = 14
            for i in range(steps + 1):
                pts += [W * i / steps, H * (base - amp * (0.3 + rnd.random() * 0.7))]
            pts += [W, H * base]
            c.create_polygon(pts, fill=col, outline="", tags="bg")
        # uzak ve orta ağaçlar
        for i in range(int(W / 26)):
            h = H * (0.12 + rnd.random() * 0.07)
            self.pine(i * 26 + rnd.randint(-8, 8), H * 0.72, h, h * 0.55, "#2c5f5d", "#3a7370")
        for i in range(int(W / 70)):
            h = H * (0.26 + rnd.random() * 0.1)
            self.pine(i * 70 + rnd.randint(-20, 20), H * 0.80, h, h * 0.5, "#1d4d3e", "#27614e")
        # zemin
        gtop = int(H * 0.80)
        n = 24
        for i in range(n):
            c.create_rectangle(0, gtop + (H - gtop) * i / n, W, gtop + (H - gtop) * (i + 1) / n + 2,
                               fill=lerp("#3f6f2e", "#14301a", i / (n - 1)), outline="", tags="bg")
        for _ in range(220):
            x = rnd.random() * W
            y = gtop + rnd.random() * (H - gtop)
            ln = (4 + rnd.random() * 8) * self.k
            c.create_line(x, y, x + rnd.uniform(-3, 3), y - ln,
                          fill=lerp("#4f8a36", "#2a5a24", rnd.random()), tags="bg")
        # ön plan büyük ağaçlar
        for fx in (0.34, 0.5, 0.62):
            h = H * 0.78
            self.pine(W * fx, H * 0.86, h, h * 0.34, "#0c2a1c", "#133a27", "#2a1a0d")
        c.tag_lower("bg")

    def draw_fireflies(self):
        c, k = self.canvas, self.k
        for bx, by, ph in self.fireflies:
            x = bx * self.W + math.sin(self.frame * 0.02 + ph) * 20 * k
            y = by * self.H + math.cos(self.frame * 0.017 + ph * 2) * 14 * k
            p = (math.sin(self.frame * 0.06 + ph) + 1) / 2
            r = (2 + 2 * p) * k
            c.create_oval(x - r * 2.4, y - r * 2.4, x + r * 2.4, y + r * 2.4,
                          fill=lerp("#2a3d1e", "#5d7a2c", p), outline="", tags="dyn")
            c.create_oval(x - r, y - r, x + r, y + r,
                          fill=lerp("#b8cf6a", "#fff9b0", p), outline="", tags="dyn")

    # ---------------------------------------------------------- çizim
    def draw_dart(self, cx, cy, ang, s):
        c = self.canvas
        dx, dy = math.cos(ang), -math.sin(ang)
        nx, ny = -dy, dx

        def Pt(x, y):
            return (cx + (dx * x + nx * y) * s, cy + (dy * x + ny * y) * s)

        def poly(pts, fill):
            flat = [v for p in pts for v in Pt(*p)]
            c.create_polygon(flat, fill=fill, outline="", tags="dyn")

        poly([(-70, 0), (-112, -22), (-122, -14), (-100, 0)], "#a3162f")
        poly([(-70, 0), (-112, 22), (-122, 14), (-100, 0)], "#ff5c7a")
        poly([(-70, 0), (-108, -4), (-120, 0), (-100, 0)], "#7d0f23")
        poly([(-70, 0), (-100, 0), (-112, -22), (-96, -26), (-70, -4)], "#e8264b")
        poly([(-52, -2.5), (-72, -2.5), (-72, 2.5), (-52, 2.5)], "#222222")
        poly([(-18, -4.5), (-54, -4.5), (-54, 4.5), (-18, 4.5)], "#c9961a")
        poly([(-18, -4.5), (-54, -4.5), (-54, -1), (-18, -1)], "#ffe27a")
        poly([(-18, 2), (-54, 2), (-54, 4.5), (-18, 4.5)], "#8a6410")
        for gx in range(-24, -52, -5):
            c.create_line(*Pt(gx, -4.5), *Pt(gx, 4.5), fill="#6b4c08", tags="dyn")
        poly([(0, 0), (-18, -2.8), (-18, 2.8)], "#d9dde3")
        poly([(0, 0), (-18, -2.8), (-18, 0)], "#ffffff")

    def draw_board(self):
        c, P, k = self.canvas, self.P, self.k
        tx, ty = self.target_x, self.target_y
        c.create_oval(*P(tx - 20, GY - 4, tx + 52, GY + 10), fill="#10260f", outline="", tags="dyn")
        c.create_rectangle(*P(tx + 2, 40, tx + 16, GY + 2), fill="#4a321c", outline="#2c1c0e", tags="dyn")
        c.create_rectangle(*P(tx + 2, 40, tx + 7, GY + 2), fill="#6a4727", outline="", tags="dyn")
        c.create_rectangle(*P(tx - 2, ty - 6, tx + 20, ty + 6), fill="#8a8f98", outline="#555", tags="dyn")
        c.create_oval(*P(tx - 24 + 8, ty - 72, tx + 24 + 8, ty + 72), fill="#0a0b0d", outline="", tags="dyn")
        rings = [(70, "#14161a"), (62, "#efe6c8"), (52, "#c4122f"), (38, "#efe6c8"),
                 (27, "#1b8a3a"), (14, "#c4122f"), (6, "#1b8a3a")]
        for ry, col in rings:
            rx = ry * 0.42
            c.create_oval(*P(tx - rx, ty - ry, tx + rx, ty + ry), fill=col, outline="#2a2a2a", tags="dyn")
        c.create_oval(*P(tx - 7, ty - 36, tx - 3, ty - 26), fill="#ffffff", outline="", tags="dyn")

    def draw_archer(self):
        c, P, k = self.canvas, self.P, self.k
        ax = 80
        a, (sx, sy), (hx, hy), (tipx, tipy) = self.pose()

        def poly(pts, fill):
            c.create_polygon(*P(*pts), fill=fill, outline="", tags="dyn")

        c.create_oval(*P(ax - 34, GY - 6, ax + 44, GY + 8), fill="#10260f", outline="", tags="dyn")
        poly((ax - 8, 340, ax - 40, 418, ax - 22, 432, ax + 2, 414), "#1b4a28")           # pelerin
        c.create_rectangle(*P(ax - 14, 408, ax - 2, 462), fill="#3e3225", outline="", tags="dyn")
        poly((ax - 18, 456, ax + 4, 456, ax + 8, 470, ax - 20, 470), "#4a2e17")
        c.create_rectangle(*P(ax + 3, 408, ax + 16, 462), fill="#54402b", outline="", tags="dyn")
        poly((ax - 1, 456, ax + 22, 456, ax + 28, 470, ax - 2, 470), "#5e3a1c")
        poly((ax - 22, 348, ax - 11, 342, ax, 392, ax - 12, 398), "#6b4423")              # sadak
        for ox, ex, ey in ((-16, -28, 316), (-13, -20, 312), (-19, -34, 322)):
            c.create_line(*P(ax + ox, 346, ax + ex, ey), width=2 * k, fill="#d9c7a0", tags="dyn")
            poly((ax + ex - 3, ey - 2, ax + ex + 4, ey - 2, ax + ex + 1, ey + 12), "#d8334a")
        poly((ax - 14, 338, ax + 16, 338, ax + 19, 414, ax - 17, 414), "#2f7d3e")         # gövde
        poly((ax + 4, 338, ax + 16, 338, ax + 19, 414, ax + 4, 414), "#3a9650")
        c.create_rectangle(*P(ax - 17, 398, ax + 19, 407), fill="#5b3a1e", outline="", tags="dyn")
        c.create_rectangle(*P(ax - 3, 397, ax + 5, 408), fill=GOLD, outline="", tags="dyn")
        c.create_line(*P(ax - 6, 348, ax - 12, 394), width=9 * k, fill="#256b34",
                      capstyle=tk.ROUND, tags="dyn")
        c.create_oval(*P(ax - 13, 301, ax + 17, 333), fill="#f0c9a0", outline="", tags="dyn")  # kafa
        poly((ax - 17, 334, ax - 16, 300, ax - 2, 288, ax + 14, 296, ax + 18, 308,
              ax + 8, 304, ax - 2, 308, ax - 5, 336), "#1d5a2c")                             # kapüşon
        c.create_oval(*P(ax + 8, 314, ax + 12, 319), fill="#222", outline="", tags="dyn")
        c.create_line(*P(ax - 4, 291, ax - 24, 272), width=3 * k, fill="#d8334a", tags="dyn")
        poly((ax - 24, 272, ax - 14, 273, ax - 20, 281), "#ff6b81")
        # atan kol
        c.create_line(*P(sx, sy, hx, hy), width=10 * k, fill="#2f7d3e", capstyle=tk.ROUND, tags="dyn")

        # dart
        if self.state in ("aim", "charge"):
            self.draw_dart(tipx * k, tipy * k, a, DS * k)
        elif self.state == "fly":
            d = self.dart
            self.draw_dart(d["x"] * k, d["y"] * k, math.atan2(-d["vy"], d["vx"]), DS * k)
        elif self.state == "stuck":
            d = self.dart
            self.draw_dart(d["x"] * k, (self.target_y + d["dy"]) * k, 0, DS * k)
            # isabet puanı etiketi
            c.create_text((self.target_x - 40) * k, (self.target_y - 90) * k,
                          text=f"+{self.hit_points}", fill=GOLD,
                          font=self.fd(self.s(26)), tags="dyn")
        if self.state in ("aim", "charge"):
            c.create_oval(*P(hx - 6, hy - 6, hx + 6, hy + 6), fill="#f0c9a0", outline="", tags="dyn")

        # nişan rehberi (noktalı çizgi): gücün ilk kısmını gösterir
        if self.state == "charge":
            pts = self.predict(self.power)
            show = int(len(pts) * 0.45)
            for i in range(0, show, 3):
                x, y = pts[i]
                r = max(1.5, (4 - 3 * i / max(1, show))) * k
                c.create_oval((x) * k - r, y * k - r, x * k + r, y * k + r,
                              fill="#ffe9a8", outline="", tags="dyn")

    # ------------------------------------------------------------ HUD
    def pill(self, x1, y1, x2, y2):
        rrect(self.canvas, x1, y1, x2, y2, 14 * self.k, fill=NAVY2, outline=GOLD2, width=2, tags="dyn")

    def cbtn(self, x1, y1, x2, y2, text, fill, cmd, size=10, fg="white"):
        c = self.canvas
        hov = x1 <= self.mx <= x2 and y1 <= self.my <= y2
        col = lerp(fill, "#ffffff", 0.18) if hov else fill
        rrect(c, x1, y1 + 3, x2, y2 + 3, 10 * self.k, fill=lerp(fill, "#000000", 0.55), outline="", tags="dyn")
        rrect(c, x1, y1, x2, y2, 10 * self.k, fill=col, outline=lerp(fill, "#ffffff", 0.45), tags="dyn")
        c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, fill=fg,
                      font=self.fb(self.s(size), "bold"), tags="dyn")
        self.buttons.append((x1, y1, x2, y2, cmd))
        return hov

    def draw_hud(self):
        c, k, W, H = self.canvas, self.k, self.W, self.H
        m = 18 * k
        anyhov = False

        # puan
        self.pill(m, m, m + 190 * k, m + 54 * k)
        c.create_text(m + 16 * k, m + 14 * k, text="PUAN", anchor="w", fill=GOLD,
                      font=self.fb(self.s(9), "bold"), tags="dyn")
        c.create_text(m + 16 * k, m + 37 * k, text=str(self.score), anchor="w", fill=TEXT,
                      font=self.fd(self.s(20)), tags="dyn")
        # can (dolu kalp = kırmızı ♥, boş kalp = soluk ♡)
        x0 = m + 206 * k
        self.pill(x0, m, x0 + 200 * k, m + 54 * k)
        c.create_text(x0 + 16 * k, m + 14 * k, text="CAN", anchor="w", fill=GOLD,
                      font=self.fb(self.s(9), "bold"), tags="dyn")
        for i in range(5):
            full = i < self.lives
            c.create_text(x0 + (24 + i * 34) * k, m + 37 * k, text="♥" if full else "♡",
                          fill="#ff4d6d" if full else "#7d8bc9",
                          font=self.fb(self.s(20), "bold"), tags="dyn")
        # süre
        tw = 190 * k
        x1 = W - m - tw
        self.pill(x1, m, W - m, m + 54 * k)
        mm, ss = self.time_left // 60, self.time_left % 60
        low = self.time_left <= 60
        tcol = TEXT if not low or (self.frame // 20) % 2 == 0 else "#ff5a5a"
        c.create_text(x1 + tw / 2, m + 24 * k, text=f"{mm:02d}:{ss:02d}", fill=tcol,
                      font=(self.mono, self.s(22), "bold"), tags="dyn")
        frac = self.time_left / GAME_TIME
        bx1, bx2, by = x1 + 16 * k, W - m - 16 * k, m + 43 * k
        rrect(c, bx1, by, bx2, by + 5 * k, 2 * k, fill="#1a2766", outline="", tags="dyn")
        if frac > 0:
            rrect(c, bx1, by, bx1 + (bx2 - bx1) * frac, by + 5 * k, 2 * k,
                  fill=lerp("#e04040", "#2ecc71", frac), outline="", tags="dyn")

        # butonlar
        by1 = m + 66 * k
        by2 = by1 + 34 * k
        x = m
        for label, wid, col, cmd in (
                ("📖 NASIL OYNANIR", 160, "#26327a", self.show_rules_window),
                ("🏅 SKOR TABLOSU", 150, "#26327a", self.show_analytics_window),
                ("⏸ DURAKLAT" if not self.is_paused else "▶ DEVAM", 120, "#b8433a" if not self.is_paused else GREEN, self.toggle_pause),
                ("🔄 YENİDEN BAŞLAT", 160, "#3b3f6a", self.restart_game)):
            if self.cbtn(x, by1, x + wid * k, by2, label, col, cmd, 9):
                anyhov = True
            x += (wid + 8) * k

        # güç barı
        bw, bh = 400 * k, 18 * k
        px1 = W / 2 - bw / 2
        py1 = H - 18 * k - 58 * k - 38 * k
        n = 40
        for i in range(n):
            t = i / (n - 1)
            col = grad(t, [(0, "#2ecc71"), (0.55, "#f1c40f"), (1, "#e74c3c")])
            if t > self.power or self.state not in ("charge",):
                col = lerp(col, "#0a1030", 0.78)
            c.create_rectangle(px1 + bw * i / n, py1, px1 + bw * (i + 1) / n - 1, py1 + bh,
                               fill=col, outline="", tags="dyn")
        c.create_rectangle(px1 - 2, py1 - 2, px1 + bw + 2, py1 + bh + 2, outline=GOLD2, width=2, tags="dyn")
        mk = px1 + bw * self.power
        c.create_polygon(mk - 7 * k, py1 - 10 * k, mk + 7 * k, py1 - 10 * k, mk, py1 - 1,
                         fill=TEXT, outline="", tags="dyn")
        c.create_text(px1, py1 - 14 * k, text="GÜÇ", anchor="w", fill=GOLD,
                      font=self.fb(self.s(10), "bold"), tags="dyn")
        c.create_text(px1 + bw, py1 - 14 * k, text=f"⬆⬇  AÇI {self.angle:.0f}°", anchor="e", fill=TEXT,
                      font=self.fb(self.s(10), "bold"), tags="dyn")

        # atış butonu (ekranın en altı)
        sw, sh = 400 * k, 56 * k
        sx1 = W / 2 - sw / 2
        sy1 = H - 18 * k - sh
        if self.state == "aim":
            label, col = "🎯  BOŞLUK  •  GÜCÜ BAŞLAT", "#e8761a"
        elif self.state == "charge":
            label, col = "🎯  BOŞLUK  •  FIRLAT!", "#d8334a"
        else:
            label, col = "…", "#3a4268"
        if self.cbtn(sx1, sy1, sx1 + sw, sy1 + sh, label, col, self.shoot_arrow, 14):
            anyhov = True
        c.config(cursor="hand2" if anyhov or any(
            b[0] <= self.mx <= b[2] and b[1] <= self.my <= b[3] for b in self.buttons) else "")

        # duraklatma paneli
        if self.is_paused:
            cx, cy = W / 2, H / 2
            rrect(c, cx - 230 * k, cy - 110 * k, cx + 230 * k, cy + 110 * k, 22 * k,
                  fill=NAVY2, outline=GOLD, width=3, tags="dyn")
            c.create_text(cx, cy - 40 * k, text="DURAKLATILDI", fill=GOLD,
                          font=self.fd(self.s(28)), tags="dyn")
            self.cbtn(cx - 110 * k, cy + 10 * k, cx + 110 * k, cy + 60 * k,
                      "▶  DEVAM ET", GREEN, self.toggle_pause, 13)

    def draw_scene(self):
        self.buttons = []
        self.canvas.delete("dyn")
        self.draw_fireflies()
        self.draw_board()
        self.draw_archer()
        self.draw_hud()

    # ------------------------------------------------ soru ekranı (Milyoner)
    def hexbar(self, x1, y1, x2, y2, fill, outline, tags, width=3):
        tip = (y2 - y1) * 0.5
        ym = (y1 + y2) / 2
        pts = [x1 + tip, y1, x2 - tip, y1, x2, ym, x2 - tip, y2, x1 + tip, y2, x1, ym]
        return self.qc.create_polygon(pts, fill=fill, outline=outline, width=width, tags=tags)

    def draw_question_screen(self):
        c = self.qc
        W, H = c.winfo_width(), c.winfo_height()
        if W < 100 or H < 100 or not getattr(self, "active_question", None):
            return
        c.delete("all")
        radial_bg(c, W, H, "#030720", "#2147b8", 0.5, 0.42)
        lattice(c, W, H, "#0b1a66", 70)

        fs = lambda v: max(8, int(W / v))
        # üst bilgi
        c.create_text(W / 2, H * 0.06, text="ENDÜSTRİ MÜHENDİSLİĞİ  •  BİLGİ YARIŞMASI",
                      fill=GOLD, font=self.fd(fs(70)))
        c.create_text(W * 0.03, H * 0.06, anchor="w", text=hearts_text(self.lives),
                      fill="#ff4d6d", font=self.fb(fs(60), "bold"))
        c.create_text(W * 0.97, H * 0.06, anchor="e", text=f"PUAN  {self.score}",
                      fill=TEXT, font=self.fd(fs(70)))
        # kalan süre
        c.create_text(W * 0.97, H * 0.105, anchor="e",
                      text=f"⏱ {self.time_left // 60:02d}:{self.time_left % 60:02d}",
                      fill=GOLD2, font=self.fb(fs(90), "bold"))
        # ilerleme elmasları
        cur = self.questions_asked_in_round
        for i in range(QUESTIONS_PER_ROUND):
            cx, cy, r = W / 2 + (i - 2) * W * 0.045, H * 0.125, W * 0.012
            col = "#14246b"
            if i < len(self.round_results):
                col = GREEN if self.round_results[i] else RED
            elif i == cur:
                col = GOLD
            c.create_polygon(cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy,
                             fill=col, outline=GOLD2, width=2)
        # amblem
        er = H * 0.085
        ex, ey = W / 2, H * 0.30
        for i in range(5):
            rr = er * (1.5 - i * 0.12)
            c.create_oval(ex - rr, ey - rr, ex + rr, ey + rr, fill=lerp("#14308f", "#2c5fe0", i / 5), outline="")
        c.create_oval(ex - er, ey - er, ex + er, ey + er, fill=NAVY, outline=GOLD, width=4)
        c.create_text(ex, ey, text="?", fill=GOLD, font=self.fd(int(er * 1.0)))

        # soru çubuğu
        qy1, qy2 = H * 0.505, H * 0.635
        qx1, qx2 = W * 0.08, W * 0.92
        ym = (qy1 + qy2) / 2
        c.create_line(0, ym, qx1, ym, fill=GOLD2, width=3)
        c.create_line(qx2, ym, W, ym, fill=GOLD2, width=3)
        self.hexbar(qx1, qy1, qx2, qy2, "#07104a", GOLD, "q", 4)
        c.create_text(W / 2, ym, text=self.active_question["q"], fill=TEXT,
                      width=(qx2 - qx1) - (qy2 - qy1) - 40, justify="center",
                      font=self.fb(fs(62), "bold"))

        # şıklar
        pos = [(0.08, 0.485, 0.685, 0.775), (0.515, 0.92, 0.685, 0.775),
               (0.08, 0.485, 0.815, 0.905), (0.515, 0.92, 0.815, 0.905)]
        for i, (a, b, ya, yb) in enumerate(pos):
            x1, x2, y1, y2 = W * a, W * b, H * ya, H * yb
            ymid = (y1 + y2) / 2
            tip = (y2 - y1) * 0.5
            g = f"g{i}"
            if i % 2 == 0:
                c.create_line(0, ymid, x1, ymid, fill=GOLD2, width=2)
            else:
                c.create_line(x2, ymid, W, ymid, fill=GOLD2, width=2)
            self.hexbar(x1, y1, x2, y2, "#07104a", GOLD2, (g, f"os{i}"), 3)
            c.create_text(x1 + tip + 14, ymid, text=f"{'ABCD'[i]}:", anchor="w", fill=ORANGE,
                          font=self.fd(fs(58)), tags=(g, f"ol{i}"))
            c.create_text(x1 + tip + 14 + fs(32), ymid, text=self.options_now[i],
                          anchor="w", fill=TEXT, width=(x2 - x1) - 2 * tip - fs(32) - 28,
                          font=self.fb(fs(88), "bold"), tags=(g, f"ot{i}"))
            c.tag_bind(g, "<Button-1>", lambda e, i=i: self.check_answer(i))
            c.tag_bind(g, "<Enter>", lambda e, i=i: self.paint_option(i, True))
            c.tag_bind(g, "<Leave>", lambda e, i=i: self.paint_option(i, False))
            self.paint_option(i)

    def paint_option(self, i, hover=False):
        c = self.qc
        st = self.opt_state[i]
        if st == "correct":
            f, t, l = GREEN, "#ffffff", "#ffffff"
        elif st == "wrong":
            f, t, l = RED, "#ffffff", "#ffffff"
        elif hover:
            f, t, l = GOLD, "#0a1030", "#0a1030"
        else:
            f, t, l = "#07104a", TEXT, ORANGE
        c.itemconfig(f"os{i}", fill=f)
        c.itemconfig(f"ot{i}", fill=t)
        c.itemconfig(f"ol{i}", fill=l)
        c.config(cursor="hand2" if hover and st == "normal" else "")

    def switch_to_question_mode(self):
        if not self.game_active:
            return
        self.question_active = True
        self.canvas.pack_forget()
        self.qc.pack(fill=tk.BOTH, expand=True)
        self.load_question()

    def switch_to_archery_mode(self):
        self.qc.pack_forget()
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.question_active = False
        self.state = "aim"
        self.power = 0

    def load_question(self):
        if self.current_q_idx >= len(self.deck):
            last = self.deck[-1]["q"] if self.deck else None
            self.deck = self.build_deck()
            if len(self.deck) > 1 and self.deck[0]["q"] == last:
                self.deck[0], self.deck[1] = self.deck[1], self.deck[0]
            self.current_q_idx = 0
        self.active_question = self.deck[self.current_q_idx]
        # bu soruyu "görüldü" olarak kaydet -> sonraki oyunlarda farklı sorular gelir
        seen = load_seen()
        seen.add(self.active_question["q"])
        save_seen(seen)
        self.has_given_hint = False
        opts = list(self.active_question["options"])
        correct_text = opts[0]
        random.shuffle(opts)
        self.correct_option_index = opts.index(correct_text)
        self.options_now = opts
        self.opt_state = ["normal"] * 4
        self.draw_question_screen()

    def check_answer(self, idx):
        if not self.question_active or self.opt_state[idx] != "normal":
            return
        if idx == self.correct_option_index:
            self.opt_state[idx] = "correct"
            self.paint_option(idx)
            self.root.bell()
            self.qc.update()
            if not self.has_given_hint:
                self.score += 100
                self.consecutive_first_try_correct += 1
                txt = "Tekte bildin!  +100 puan"
                if self.consecutive_first_try_correct >= 2:
                    self.score += 50
                    txt += "\n🔥 Üst üste 2 soru tekte!  +50 bonus"
                    self.consecutive_first_try_correct = 0
            else:
                self.score += 50
                self.consecutive_first_try_correct = 0
                txt = "İpucuyla 2. şansta bildin.  +50 puan"
            self.current_round_correct += 1
            self.round_results.append(True)
            self.dialog("Doğru cevap!", txt, GREEN, "✅", "DEVAM")
            self.current_q_idx += 1
            self.questions_asked_in_round += 1
            self.check_round_completion()
        else:
            self.opt_state[idx] = "wrong"
            self.paint_option(idx)
            self.root.bell()
            self.qc.update()
            self.consecutive_first_try_correct = 0
            if not self.has_given_hint:
                self.has_given_hint = True
                self.dialog("Yanlış cevap", f"💡 İpucu: {self.active_question['hint']}\n\nBir şansın daha var!",
                            RED, "❌", "TEKRAR DENE")
            else:
                self.opt_state[self.correct_option_index] = "correct"
                self.paint_option(self.correct_option_index)
                self.qc.update()
                self.current_round_wrong += 1
                self.round_results.append(False)
                self.dialog("Yine yanlış", f"Doğru cevap:\n{self.active_question['options'][0]}",
                            RED, "❌", "DEVAM")
                self.current_q_idx += 1
                self.questions_asked_in_round += 1
                if self.lose_life():
                    return
                self.check_round_completion()

    def lose_life(self):
        """İpucuna rağmen yanlış cevapta 1 can gider. Oyun bittiyse True döner."""
        self.lives -= 1
        if self.lives <= 0:
            self.ban_until = time.time() + 300
            self.dialog("Can hakkı bitti",
                        f"{hearts_text(0)}\nTüm canlarınız bitti!\n\n5 dakika sonra tekrar deneyiniz.",
                        RED, "💔", "TAMAM")
            self.record_session_and_game_over("Canlar Tükendi (5 Dakika Ceza)")
            return True
        self.dialog("Can kaybı",
                    f"Yanlış cevap, 1 can gitti!\n\n{hearts_text(self.lives)}\n{self.lives} canınız kaldı.",
                    ORANGE, "💔", "DEVAM")
        return False

    def check_round_completion(self):
        if not self.game_active:
            return
        if self.questions_asked_in_round >= QUESTIONS_PER_ROUND:
            c, w = self.current_round_correct, self.current_round_wrong
            status = f"Turu Tamamladınız ({c} Doğru, {w} Yanlış) 🏆"
            self.dialog("Tur tamamlandı!", f"{c} doğru, {w} yanlış.\nYeni turda yeni sorular seni bekliyor!",
                        GOLD, "🏆", "DEVAM")
            self.session_data.append({"round": self.session_counter, "score": self.score,
                                      "correct": c, "wrong": w, "status": status})
            self.session_counter += 1
            self.current_round_correct = 0
            self.current_round_wrong = 0
            self.questions_asked_in_round = 0
            self.round_results = []
        self.switch_to_archery_mode()

    # ------------------------------------------------------ pencereler
    def dialog(self, title, message, color=GOLD, icon="✨", btn="TAMAM"):
        self.dialog_open = True
        top = tk.Toplevel(self.root)
        top.configure(bg=color)
        top.title(title)
        top.transient(self.root)
        top.resizable(False, False)
        inner = tk.Frame(top, bg=NAVY2)
        inner.pack(padx=3, pady=3, fill="both", expand=True)
        tk.Label(inner, text=icon, font=(self.body, 40), bg=NAVY2, fg=color).pack(pady=(22, 0))
        tk.Label(inner, text=title.upper(), font=self.fd(18), bg=NAVY2, fg=color).pack(pady=(4, 8))
        tk.Label(inner, text=message, font=self.fb(12), bg=NAVY2, fg=TEXT, wraplength=420,
                 justify="center").pack(padx=36, pady=(0, 20))
        b = tk.Button(inner, text=btn, font=self.fb(12, "bold"), bg=color, fg="#0a1030",
                      activebackground=lerp(color, "#ffffff", 0.25), relief="flat", bd=0,
                      padx=34, pady=9, cursor="hand2", command=top.destroy)
        b.pack(pady=(0, 24))
        top.bind("<Return>", lambda e: top.destroy())
        top.update_idletasks()
        w, h = top.winfo_reqwidth(), top.winfo_reqheight()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        top.geometry(f"+{max(0, x)}+{max(0, y)}")
        top.grab_set()
        b.focus_set()
        self.root.wait_window(top)
        self.dialog_open = False

    def themed_window(self, title, w, h):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=GOLD2)
        win.transient(self.root)
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        inner = tk.Frame(win, bg=NAVY2)
        inner.pack(fill="both", expand=True, padx=3, pady=3)
        return win, inner

    def show_rules_window(self):
        W, H = 800, 720
        win, f = self.themed_window("Nasıl Oynanır", W, H)
        cw, ch = W - 6, H - 6
        c = tk.Canvas(f, width=cw, height=ch, highlightthickness=0, bg=NAVY)
        c.pack(fill="both", expand=True)
        rnd = random.Random(11)

        # ---------- arka plan: gradyan, kafes, ışık halkaları
        radial_bg(c, cw, ch, "#030720", "#2a55d0", 0.5, 0.30)
        lattice(c, cw, ch, "#0e2078", 56)
        for i in range(8):
            r = 330 - i * 38
            c.create_oval(cw / 2 - r, -r * 0.55, cw / 2 + r, r * 0.55,
                          outline=lerp("#16308f", "#6b92ff", i / 8), width=1)
        for i in range(6):
            r = 260 - i * 38
            c.create_oval(cw / 2 - r, ch - r * 0.45, cw / 2 + r, ch + r * 0.45,
                          outline=lerp("#16308f", "#5b86ff", i / 6), width=1)

        # ---------- konfeti
        palette = [GOLD, "#ff5c7a", "#35e08a", "#6bb6ff", "#ff8a1f", "#ffffff", "#c58bff"]
        for _ in range(95):
            x, y = rnd.random() * cw, rnd.random() * ch
            col = rnd.choice(palette)
            kind = rnd.random()
            if kind < 0.4:
                r = rnd.choice((2, 3, 4))
                c.create_oval(x - r, y - r, x + r, y + r, fill=col, outline="")
            elif kind < 0.8:
                a = rnd.random() * 6.28
                w, h = rnd.choice((4, 5, 7)), rnd.choice((2, 3))
                pts = []
                for dx, dy in ((-w, -h), (w, -h), (w, h), (-w, h)):
                    pts += [x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a)]
                c.create_polygon(pts, fill=col, outline="")
            else:
                r = rnd.choice((4, 6, 8))
                c.create_polygon(x, y - r, x + r * 0.3, y - r * 0.3, x + r, y, x + r * 0.3, y + r * 0.3,
                                 x, y + r, x - r * 0.3, y + r * 0.3, x - r, y, x - r * 0.3, y - r * 0.3,
                                 fill=col, outline="")

        # ---------- köşelerde dart tahtaları
        def board(cx, cy, R):
            cols = ["#14161a", "#efe6c8", "#c4122f", "#efe6c8", "#1b8a3a", "#c4122f", "#1b8a3a"]
            c.create_oval(cx - R - 7, cy - R - 7, cx + R + 7, cy + R + 7, fill="#050b2e", outline=GOLD2, width=3)
            for i, col in enumerate(cols):
                r = R * (1 - i * 0.14)
                c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=col, outline="#2a2a2a")
        board(34, 34, 56)
        board(cw - 34, 34, 56)
        board(34, ch - 34, 44)
        board(cw - 34, ch - 34, 44)

        # ---------- çerçeve + köşe elmasları
        c.create_rectangle(8, 8, cw - 8, ch - 8, outline=GOLD2, width=3)
        c.create_rectangle(16, 16, cw - 16, ch - 16, outline=GOLD2, width=1)
        for x, y in ((cw / 2, 12), (cw / 2, ch - 12), (12, ch / 2), (cw - 12, ch / 2)):
            c.create_polygon(x, y - 8, x + 8, y, x, y + 8, x - 8, y, fill=GOLD, outline=NAVY, width=2)

        # ---------- başlık şeridi + kurdele uçları
        tx1, tx2, ty1, ty2 = cw * 0.18, cw * 0.82, 28, 100
        tip = (ty2 - ty1) / 2
        ym = (ty1 + ty2) / 2
        c.create_polygon(tx1 - 40, ym - 18, tx1 + 10, ym - 18, tx1 + 10, ym + 18, tx1 - 40, ym + 18, tx1 - 22, ym,
                         fill="#8a1f3a", outline=GOLD2, width=2)
        c.create_polygon(tx2 + 40, ym - 18, tx2 - 10, ym - 18, tx2 - 10, ym + 18, tx2 + 40, ym + 18, tx2 + 22, ym,
                         fill="#8a1f3a", outline=GOLD2, width=2)
        c.create_polygon(tx1 + tip, ty1, tx2 - tip, ty1, tx2, ym, tx2 - tip, ty2, tx1 + tip, ty2, tx1, ym,
                         fill="#07104a", outline=GOLD, width=4)
        c.create_polygon(tx1 + tip + 6, ty1 + 6, tx2 - tip - 6, ty1 + 6, tx2 - 8, ym, tx2 - tip - 6, ty2 - 6,
                         tx1 + tip + 6, ty2 - 6, tx1 + 8, ym, fill="", outline=GOLD2, width=1)
        c.create_text(cw / 2, 58, text="🎯  NASIL OYNANIR  🎯", font=self.fd(24), fill=GOLD)
        c.create_text(cw / 2, 85, text="ENDÜSTRİ MÜHENDİSLİĞİ  •  DART CHALLENGE",
                      font=self.fb(9, "bold"), fill="#9db8ff")

        # ---------- kural kartları
        rows = [
            ("🎯", "#c4122f", "BOŞLUK ile güç barını başlat, doğru anda tekrar BOŞLUK ile fırlat. ⬆️⬇️ tuşları açıyı ayarlar."),
            ("✨", "#6b4fd8", "Noktalı çizgi dartın yolunu gösterir. Yerçekimini unutma!"),
            ("⭐", "#d99a1e", None),
            ("🧠", "#1fa64a", "Soruyu tek seferde bilirsen +100, ipucuyla bilirsen +50. Üst üste 2 soruyu tekte bilirsen +50 bonus."),
            ("❓", "#2d7be0", "Her tur 5 soru, her turda farklı sorular gelir. A, B, C, D tuşlarıyla da cevap verebilirsin."),
            ("💔", "#e04040", "İpucuna rağmen yanlış yaparsan 1 can (♥) gider. 5 can da biterse 5 dakika sonra tekrar deneyiniz."),
            ("💨", "#ff8a1f", "Iskalarsan puan alamazsın ama oyun bitmez, tekrar atabilirsin."),
            ("⏱", "#17a2b8", "Toplam süre 5 dakika. Süre bitince oyun biter, en yüksek puanı yapmaya çalış!"),
            ("⌨️", "#7d8bc9", "P: duraklat  •  Esc / F11: tam ekran aç-kapa"),
        ]
        chips = [("50", "Bullseye", "#1b8a3a", "#ffffff"), ("25", "Dış bull", "#c4122f", "#ffffff"),
                 ("20", "Yeşil", "#1b8a3a", "#ffffff"), ("15", "Krem", "#efe6c8", "#14161a"),
                 ("10", "Kırmızı", "#c4122f", "#ffffff"), ("5", "Dış krem", "#efe6c8", "#14161a"),
                 ("1", "Kenar", "#14161a", "#ffffff")]
        y = 116
        gap = 7
        x1, x2 = 34, cw - 34
        for ic, accent, tx in rows:
            rh = 66 if tx is None else 50
            c.create_polygon(x1 + 6, y + 5, x2 + 6, y + 5, x2 + 6, y + rh + 5, x1 + 6, y + rh + 5,
                             fill="#020619", outline="")
            rrect(c, x1, y, x2, y + rh, 14, fill="#0a1a66", outline=GOLD2, width=2)
            rrect(c, x1 + 4, y + 4, x1 + 62, y + rh - 4, 11, fill=accent, outline=lerp(accent, "#ffffff", 0.5), width=1)
            c.create_text(x1 + 33, y + rh / 2, text=ic, font=(self.body, 20), fill="#ffffff")
            if tx is not None:
                c.create_text(x1 + 78, y + rh / 2, text=tx, anchor="w", fill=TEXT,
                              width=x2 - x1 - 96, font=self.fb(11, "bold"))
            else:
                c.create_text(x1 + 76, y + 13, text="DART PUANLARI (merkeze yaklaştıkça puan artar)", anchor="w",
                              fill=GOLD, font=self.fb(9, "bold"))
                span = (x2 - 14) - (x1 + 96)
                for i, (pt, nm, col, fg) in enumerate(chips):
                    cx = x1 + 96 + span * (i + 0.5) / len(chips) - 10
                    cy = y + 38
                    c.create_oval(cx - 14, cy - 14, cx + 14, cy + 14, fill=col, outline=GOLD2, width=2)
                    c.create_text(cx, cy, text=pt, fill=fg, font=self.fb(10, "bold"))
                    c.create_text(cx + 18, cy, text=nm, anchor="w", fill=TEXT, font=self.fb(8))
            y += rh + gap

        # ---------- buton
        btn = tk.Button(win, text="ANLADIM, OYNAYALIM!  🎯", font=self.fb(12, "bold"), bg=GOLD,
                        fg="#0a1030", activebackground=lerp(GOLD, "#ffffff", 0.3), relief="flat",
                        bd=0, padx=30, pady=8, cursor="hand2", command=win.destroy)
        c.create_window(cw / 2, ch - 38, window=btn)
        win.bind("<Return>", lambda e: win.destroy())
        win.bind("<Escape>", lambda e: win.destroy())
        btn.focus_set()

    def show_analytics_window(self):
        win, f = self.themed_window("Skor Tablosu", 820, 540)
        tk.Label(f, text="SKOR TABLOSU", font=self.fd(22), bg=NAVY2, fg=GOLD).pack(pady=(20, 12))
        body = tk.Frame(f, bg=NAVY2)
        body.pack(fill="both", expand=True, padx=24)
        widths = [10, 10, 18, 40]
        for i, (h, w) in enumerate(zip(["OTURUM", "PUAN", "DOĞRU / YANLIŞ", "DURUM"], widths)):
            tk.Label(body, text=h, width=w, font=self.fb(10, "bold"), bg=BLUE, fg="white").grid(
                row=0, column=i, padx=1, pady=1, ipady=6)
        if not self.session_data:
            tk.Label(body, text="Henüz tamamlanan oturum yok.", bg=NAVY2, fg=TEXT,
                     font=self.fb(11)).grid(row=1, column=0, columnspan=4, pady=40)
        for r, d in enumerate(self.session_data, start=1):
            ok = d["status"].startswith("Turu Tamamladınız")
            vals = [d["round"], d["score"], f"{d['correct']} D / {d['wrong']} Y", d["status"]]
            for i, (v, w) in enumerate(zip(vals, widths)):
                tk.Label(body, text=v, width=w, font=self.fb(10), bg="#0e1c5c",
                         fg=(("#4dffb0" if ok else "#ff7a7a") if i == 3 else TEXT)).grid(
                    row=r, column=i, padx=1, pady=1, ipady=5)
        tk.Button(f, text="KAPAT", font=self.fb(12, "bold"), bg=GOLD, fg="#0a1030", relief="flat",
                  bd=0, padx=30, pady=8, cursor="hand2", command=win.destroy).pack(pady=18)

    # --------------------------------------------------- zaman / durum
    def start_timer(self):
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None
        self._tick()

    def _tick(self):
        if not self.game_active:
            return
        try:
            if not self.is_paused and not self.dialog_open:
                if self.time_left <= 0:
                    self.record_session_and_game_over("Süre Bitti")
                    return
                self.time_left -= 1
            self.timer_job = self.root.after(1000, self._tick)
        except tk.TclError:
            pass

    def toggle_pause(self):
        if self.game_active and not self.question_active:
            self.is_paused = not self.is_paused

    # ----------------------------------------------------------- oyun sonu
    def record_session_and_game_over(self, status="Oyunu Kaybettiniz"):
        if not self.game_active:
            return
        self.game_active = False
        if self.current_round_correct + self.current_round_wrong > 0:
            self.session_data.append({"round": self.session_counter, "score": self.score,
                                      "correct": self.current_round_correct,
                                      "wrong": self.current_round_wrong, "status": status})
            self.session_counter += 1
        self.dialog_open = True
        W, H = 720, 520
        win = tk.Toplevel(self.root)
        win.title("Oyun Sonu")
        win.transient(self.root)
        win.resizable(False, False)
        x = self.root.winfo_rootx() + (self.root.winfo_width() - W) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - H) // 2
        win.geometry(f"{W}x{H}+{max(0, x)}+{max(0, y)}")
        c = tk.Canvas(win, width=W, height=H, highlightthickness=0, bg=NAVY)
        c.pack()
        radial_bg(c, W, H, "#030720", "#2a55d0", 0.5, 0.4)
        lattice(c, W, H, "#0e2078", 56)
        won = self.score >= WIN_SCORE
        col = "#35e08a" if won else "#ff6b6b"
        c.create_rectangle(8, 8, W - 8, H - 8, outline=GOLD2, width=3)
        c.create_rectangle(16, 16, W - 16, H - 16, outline=GOLD2, width=1)
        c.create_text(W / 2, 92, text="🏆" if won else "💥", font=(self.body, 56))
        c.create_text(W / 2, 168, text="TEBRİKLER!" if won else "OYUN BİTTİ",
                      font=self.fd(34), fill=col)
        c.create_text(W / 2, 210, text=status, font=self.fb(11), fill="#b9c4ff")
        c.create_text(W / 2, 258, text="TOPLAM PUAN", font=self.fb(11, "bold"), fill=GOLD)
        c.create_text(W / 2, 312, text=str(self.score), font=self.fd(52), fill=TEXT)
        c.create_text(W / 2, 372, text="Yeniden oynamak ister misiniz?", font=self.fb(13), fill="#dfe6ff")

        def yes():
            self.dialog_open = False
            win.destroy()
            self.restart_game()

        def no():
            self.dialog_open = False
            win.destroy()
            self.root.destroy()

        def mk(text, color, cmd, fg="white"):
            return tk.Button(win, text=text, font=self.fb(12, "bold"), bg=color, fg=fg,
                             activebackground=lerp(color, "#ffffff", 0.2), relief="flat", bd=0,
                             padx=22, pady=10, cursor="hand2", command=cmd)

        c.create_window(W / 2 - 110, 440, window=mk("✅  YENİDEN BAŞLAT", GREEN, yes))
        c.create_window(W / 2 + 130, 440, window=mk("ÇIK", "#b8433a", no))
        win.protocol("WM_DELETE_WINDOW", no)
        win.grab_set()
        self.root.wait_window(win)

    def restart_game(self):
        if time.time() < self.ban_until:
            rem = int(self.ban_until - time.time())
            self.dialog("Ceza süresi", f"Henüz dolmadı!\n{rem // 60} dakika {rem % 60} saniye beklemelisiniz.",
                        RED, "⏳")
            return
        self.new_game_state()
        self.switch_to_archery_mode()
        self.start_timer()


if __name__ == "__main__":
    root = tk.Tk()
    DartGame(root)
    root.mainloop()
