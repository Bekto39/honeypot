import pandas as pd
import matplotlib.pyplot as plt
import os

# --- AYARLAR ---
json_dosya_yolu = "cowrie_data.json" 
csv_dosya_yolu = "zararli_ip_raporu.csv"

# Grafik stili
plt.style.use('ggplot')

print("Veriler Yükleniyor, lütfen bekleyin...")

try:
    df = pd.read_json(json_dosya_yolu, lines=True)
    print(f"-> Toplam Log Sayısı: {len(df)}")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except ValueError:
    print("Hata: JSON bozuk veya dosya boş.")
    exit()
except FileNotFoundError:
    print(f"Hata: {json_dosya_yolu} bulunamadı. Dosya ismini kontrol et.")
    exit()

# --- ÜLKE ANALİZİ ---

if os.path.exists(csv_dosya_yolu):
    df_csv = pd.read_csv(csv_dosya_yolu)
    ip_ulke_map = df_csv.set_index('src_ip')['country'].to_dict()
    df['country'] = df['src_ip'].map(ip_ulke_map)
    
    if 'country' in df.columns:
        filtered_df = df[~df['country'].isin(['Hata', 'Bilinmiyor', 'Fail', 'None'])]
        top_countries = filtered_df['country'].value_counts().head(10)

        plt.figure(figsize=(12, 6))
        ax = top_countries.plot(kind='bar', color='#1f77b4')
        plt.title(f'En Çok Saldıran 10 Ülke', fontsize=14)
        plt.xlabel('Ülke')
        plt.ylabel('Saldırı Sayısı')
        plt.xticks(rotation=45)
        
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
else:
    print("UYARI: 'zararli_ip_raporu.csv' bulunamadı. Ülke grafiği atlanıyor.")


# --- SAATLİK ANALİZ ---
df['hour'] = df['timestamp'].dt.hour
hourly_counts = df['hour'].value_counts().sort_index()
saat_etiketleri = [f"{i:02d}:00" for i in range(24)]

plt.figure(figsize=(14, 6))
hourly_counts.reindex(range(24), fill_value=0).plot(kind='line', marker='o', color='#d62728', linewidth=2)
plt.title('Günlük Saldırı Yoğunluğu (Saatlik Botnet Aktivitesi)', fontsize=14)
plt.xlabel('Saat')
plt.ylabel('Saldırı Sayısı')
plt.xticks(range(24), saat_etiketleri, rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# --- KULLANICI ADI & ŞİFRE ---
girisler = df[df['eventid'] == 'cowrie.login.failed']

if not girisler.empty:
    top_users = girisler['username'].value_counts().head(10).sort_values()
    top_pass = girisler['password'].value_counts().head(10).sort_values()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    top_users.plot(kind='barh', color='#1f77b4', ax=axes[0])
    axes[0].set_title('En Çok Denenen 10 Kullanıcı Adı')
    axes[0].set_xlabel('Deneme Sayısı')
    
    top_pass.plot(kind='barh', color='#2ca02c', ax=axes[1])
    axes[1].set_title('En Çok Denenen 10 Şifre')
    axes[1].set_xlabel('Deneme Sayısı')

    plt.tight_layout()
    plt.show()


# --- KOMUT ANALİZİ  ---

if 'input' in df.columns:
    komutlar = df[df['eventid'] == 'cowrie.command.input']['input']
    
    if not komutlar.empty:
        top_commands = komutlar.value_counts().head(15).sort_values()

        plt.figure(figsize=(14, 8)) 
        ax = top_commands.plot(kind='barh', color='#9467bd')
        
        plt.title('Saldırganların Çalıştırdığı Komutlar (Botnet İmzası)', fontsize=15)
        plt.xlabel('Tekrar Sayısı')
        plt.ylabel('Komut İçeriği')
        
        for p in ax.patches:
            ax.annotate(str(p.get_width()), 
                        (p.get_width(), p.get_y() + p.get_height()/2),
                        xytext=(5, 0), textcoords='offset points',
                        ha='left', va='center', fontsize=10, fontweight='bold')
            
        plt.tight_layout()
        plt.show()
    else:
        print("Komut verisi bulunamadı.")


# ---  SSH VERSİYON  ---

if 'version' in df.columns:
    versiyonlar = df[df['eventid'] == 'cowrie.client.version']['version']
    versiyonlar = versiyonlar.str.split(' ').str[0]
    
    counts = versiyonlar.value_counts()
    total = counts.sum()
    mask = (counts / total) > 0.02
    buyuk_dilimler = counts[mask]
    
    kucuk_dilimler_toplami = counts[~mask].sum()
    if kucuk_dilimler_toplami > 0:
        buyuk_dilimler['Diğerleri (Others)'] = kucuk_dilimler_toplami

    plt.figure(figsize=(10, 8))
    renkler = plt.get_cmap('Pastel1')(range(len(buyuk_dilimler)))

    plt.pie(
        buyuk_dilimler, 
        labels=buyuk_dilimler.index,
        autopct='%1.1f%%', 
        startangle=140, 
        colors=renkler,
        explode=[0.05] * len(buyuk_dilimler)
    )
    plt.title('Saldırganların Kullandığı Yazılımlar', fontsize=14)
    plt.tight_layout()
    plt.show()


# ---  OTURUM SÜRESİ ANALİZİ  ---

session_groups = df.groupby('session')['timestamp']
start_times = session_groups.min()
end_times = session_groups.max()
durations = (end_times - start_times).dt.total_seconds()

durations = durations[durations > 0]

if not durations.empty:
    plt.figure(figsize=(10, 6))
    
    plt.hist(durations, bins=50, range=(0, 10), color='#17becf', edgecolor='black')
    
    plt.title('Saldırganların İçeride Kalma Süreleri (Saniye)', fontsize=14)
    plt.xlabel('Süre (Saniye)')
    plt.ylabel('Oturum Sayısı')
    plt.grid(True, alpha=0.5)
    
    plt.tight_layout()
    plt.show()
    
    print(f"-> Ortalama Oturum Süresi: {durations.mean():.2f} saniye")
    print(f"-> En Uzun Oturum: {durations.max():.2f} saniye")


# ---  ŞİFRELEME ALGORİTMALARI ---

if 'kexAlgs' in df.columns:
    kex_data = df[df['eventid'] == 'cowrie.client.kex']['kexAlgs'].explode()
    
    if not kex_data.empty:
        top_kex = kex_data.value_counts().head(10).sort_values() 
        
        plt.figure(figsize=(12, 7))
        ax = top_kex.plot(kind='barh', color='#bcbd22') 
        
        plt.title('Saldırganların Desteklediği Şifreleme Algoritmaları', fontsize=14)
        plt.xlabel('Kullanım Sayısı')
        plt.ylabel('Algoritma Adı')
        
        for p in ax.patches:
            ax.annotate(str(p.get_width()), 
                        (p.get_width(), p.get_y() + p.get_height()/2),
                        xytext=(5, 0), textcoords='offset points',
                        ha='left', va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.show()

print("\n--- TÜM ANALİZLER TAMAMLANDI ---")