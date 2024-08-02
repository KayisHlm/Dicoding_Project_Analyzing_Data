import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sidebar
with st.sidebar :
    st.write('# Identitas')
    st.write("""
            - **Nama:** [Kayis Hilmi Farih]
            - **Email:** [kayishilmi24@gmail.com]
            - **ID Dicoding:** [Kayis Hilmi Farih]
            """)
    
    st.write('# Daftar Pertanyaan')
    st.write("""
            1. Kapan waktu (jam) rata-rata peminjaman sepeda mencapai angka tertinggi ?
            2. Bagaimana kenaikan terbanyak dan penurunan terbanyak jumlah peminjaman sepeda pada tahun 2012 ?
            """)
         
st.title('ANALISIS DATA PENYEWAAN SEPEDA')
st.write('###### Pada kesempatan kali ini, saya akan menyajikan hasil',
         'analisis data dengan menggunakan dua buah dataset, yaitu',
         "'day.csv' dan 'hour.csv'.")
    
#=================Data Wrangling=================#

## Data Gathering
st.write('## Data Gathering')

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')


### Menampilkan data day.csv
st.write('#### Menampilkan data day.csv')
max_day = day_df['instant'].count()
number_day = st.number_input(label = 'Masukkan jumlah baris yang ingin ditampilkan',value=5, min_value=1,max_value= max_day,label_visibility= 'visible')
st.write(day_df.head(number_day))

### Menampilkan data hour.csv
st.write('#### Menampilkan data hour.csv')
max_hour = hour_df['instant'].count()
number_hour = st.number_input(label = 'Masukkan jumlah baris yang ingin ditampilkan',value=5, min_value=1,max_value= max_hour,label_visibility= 'visible')
st.write(hour_df.head(number_hour))

## Data Assessing
st.write('## DATA ASSESSING')

### Missing Value
st.write('#### Mencari Missing Value')
col1,col2 = st.columns([1,1])

with col1 :
    st.text('day.csv')
    st.write(day_df.isnull().sum())

with col2 :
    st.text('hour.csv')
    st.write(hour_df.isnull().sum())

### Duplicated Data
st.write('#### Mencari Duplikasi Data')
day_duplicated = day_df.duplicated().sum()
hour_duplicated = hour_df.duplicated().sum()
st.write('Jumlah data yang terduplikasi pada dataset day.csv dan hour.csv masing-masing adalah',day_duplicated,'dan',hour_duplicated)

### Table Description
st.write('#### Tabel Deskripsi Dataset')
st.text('Day.csv')
st.write(day_df.describe())

st.text('Hour.csv')
st.write(hour_df.describe())

### Outliers
st.write('#### Mencari Outliers')
st.write('Outliers filtering tidak perlu dilakukan dikarenakan seluruh informasi penting atau mendukung hipotesis.')

### Data Assessing Result
st.write('#### Hasil Data Assessing')
st.write("""
        Berdasarkan pengecekan data, ternyata tidak ditemukan adanya kesalahan tipe data, duplikasi data, 
         serta missing value dalam kedua dataset. Pencarian outlier tidak perlu dilakukan karena data yang 
         diinput merupakan data valid. Apabila dilakukan pengecekan dan penghapusan outliers, hal ini dapat 
         berefek pada hasil penyajian data yang kurang tepat. Maka, dapat disimpulkan bahwa kedua dataset 
         tersebut telah memiliki data valid yang tidak perlu dilakukan data cleaning.
        """)
## Data Cleaning
st.write('## Data Cleaning')
st.write('Karena tidak ditemukan adanya kesalahan data pada kedua dataset, maka tidak dilakukan data cleaning')

#=================EDA=================#

st.write('# Exploratory & Explanatory Data Analysis')

## No. 1
st.write('## No. 1')
st.write('Menerapkan metode RFM (Recency, Frequency, and Monetary) untuk menemukan pola jam yang paling sering dilakukan peminjaman sepeda.')
st.write("""
        Mengapa menggunakan teknik RFM ? Jawabannya adalah :

        - Membantu dalam mengevaluasi efektivitas layanan dengan melihat pola penggunaan 
         dan nilai yang dihasilkan pada berbagai waktu.

        - Mengetahui jam-jam dengan frekuensi tinggi memungkinkan pengelola layanan untuk 
         mengalokasikan sumber daya (misalnya jumlah sepeda, staf) dengan lebih efisien.

        - Dengan analisis RFM, kita dapat mengelompokkan pengguna berdasarkan perilaku mereka, 
         sehingga memudahkan dalam menargetkan promosi atau layanan khusus yang lebih tepat sasaran.

        Cara melakukan metode tersebut adalah dengan mencari nilai Recency, Frequency, dan Monetary

        1. **Recency (Kebaruan) :** Mengukur seberapa baru aktivitas terakhir pengguna. Dalam konteks 
         pinjaman sepeda, ini bisa berarti seberapa baru jam terakhir sepeda dipinjam.
         
        2. **Frequency (Frekuensi) :** Mengukur seberapa sering pengguna melakukan aktivitas tertentu 
         dalam periode waktu tertentu. Dalam contoh ini, frekuensi mengacu pada berapa kali sepeda dipinjam dalam jam tertentu
         
        3. **Monetary (Monetari) :** Mengukur seberapa banyak nilai yang dihasilkan dari aktivitas pengguna. 
         Dalam konteks pinjaman sepeda, ini bisa diterjemahkan menjadi total jumlah sepeda yang dipinjam pada jam tertentu.
        """)

### Penyajian Tabel RFM
st.write('#### Hasil Pembentukan Tabel RFM')

rfm_df = hour_df.groupby('hr').agg({
    'dteday': 'nunique',
    'cnt': ['sum', 'mean']
}).reset_index()
rfm_df.columns = ['Hour', 'Frequency', 'Total_Bike', 'Average_Bike']
rfm_df['Recency'] = rfm_df['Hour']
rfm_df.sort_values(by='Total_Bike', ascending=False, inplace=True)
rfm_df.set_index('Hour', inplace=True)
st.write(rfm_df)

### Langkah Penyelesaian
if st.button('Tampilkan Langkah Penyelesaian No. 1') :
    tab1,tab2,tab3,tab4 = st.tabs(['Langkah 1','Langkah 2','Langkah 3','Langkah 4'])
     
    with tab1:
        code = """rfm_df = hour_df.groupby('hr').agg({
        'dteday': 'nunique',
        'cnt': ['sum', 'mean']
        }).reset_index()
        """
        st.code(code, language='python')
        st.write("""
                 Membuat pivot table dengan jam (hr) sebagai parameter dengan kolom 'dteday' 
                 dengan value 'nunique' atau count hari unik. kolom yang kedua adalah 'cnt' 
                 dengan value jumlah atau sum, dan rata-rata atau mean. Kemudian dilakukan 
                 reset index untuk menyamakan index dengan urutan jam atau 'hr'.
                """)
    with tab2:
        code = """
        rfm_df.columns = ['Hour', 'Frequency', 'Total_Bike', 'Average_Bike']       
        """
        st.code(code,language='python')
        st.write("""
                 Mengubah nama kolom menyesuaikan dengan metode RFM. Kolom 'hr' diubah menjadi 'Hour', 
                 'dteday nunique' menjadi 'Frequency' (berperan ssebagai Frequency dalam RFM). Nah disini, 
                 'cnt sum' dan 'cnt mean' berperan menjadi satu sebagai Monetary dalam RFM, kemudian 
                 masing-masing diubah nama menjadi 'Total_Bike' dan 'Average_Bike'.
                """)
    with tab3:
        code = """
        rfm_df['Recency'] = rfm_df['Hour']
        """
        st.code(code, language='python')
        st.write("""
                 Untuk memasukkan bagian Recency dalam RFM, kita hanya perlu membuat kolom baru dengan value 
                 yang sama dengan Hour karena kita berurusan dengan spesifikasi jam.
                """)
    with tab4:
        code = """
        rfm_df.sort_values(by='Total_Bike', ascending=False, inplace=True)
        rfm_df.set_index('Hour', inplace=True)
        """
        st.code(code, language='python')
        st.write("""
                 Mengurutkan tabel rfm_df berdasarkan value kolom 'Total_Bike' secara menurun sehingga data 
                 teratas adalah data dengan nilai 'Total_Bike' tertinggi. Selain itu, untuk meringkas tabel, 
                 kita menjadikan kolom 'Hour' sebagai index.
                """)
### Data Visualization
st.write("### Visualisasi Data")
tab1,tab2 = st.tabs(['Tab 1','Tab 2'])

with tab1:
    st.header("Total Sepeda Disewakan")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(rfm_df.index, rfm_df['Total_Bike'], color='lightgreen')
    ax.set_xlabel('Jam per-Hari')
    ax.set_title('Total Sepeda yang Disewa per-Jam')
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.header("Rata-rata Sepeda Disewakan")
    fig,ax = plt.subplots(figsize=(12,6))
    ax.bar(rfm_df.index, rfm_df['Average_Bike'], color='salmon')
    ax.set_xlabel('Jam per-Hari')
    ax.set_title('Total Sepeda yang Disewa per-Jam')
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)

### Result

st.write('#### Hasil Analisis')
The_Most_Rented_Hour = rfm_df.head(3)
st.write(The_Most_Rented_Hour)

### Conclusion

with st.expander('Kesimpulan'):
        st.write("""
                Berdasarkan analisis data yang dilakukan terhadap dataset hour.csv, ditemukan kesimpulan 
                bahwa rata-rata tertinggi penyewaan sepeda dilakukan pada 3 waktu tertentu selama periode tahun 2011-2012.

                Yang pertama, pukul 17.00 adalah waktu yang paling banyak terjadi penyewaan sepeda dengan total 336.860 dan rata-rata penyewa 461,452055.

                Yang kedua adalah pukul 18.00 dengan total 309.772 dan rata-rata 425,510989.

                Dan yang ketiga adalah pukul 08.00 dengan total 261.001 dan rata-rata 359,011004.
                """)

## No. 2
st.write('## No. 2')

st.write("""
        Langkah pertama untuk mengetahui kenaikan dan penurunan yang terjadi adalah dengan mencari data 
        mengenai selisih jumlah penyewa dari bulan satu ke bulan berikutnya.
        """)

st.write('#### Hasil Pembentukan Tabel')
day_df = day_df[day_df['yr'] == 1]
def selisih(x):
  lst = []
  for i in range(len(x)-1):
    if x[i] > x[i+1]:
      c = (x[i] - x[i+1]) * -1
      lst.append(c)
    elif x[i] < x[i+1]:
      c = x[i+1] - x[i]
      lst.append(c)
  return lst
result = day_df.groupby(by='mnth').agg({
    'cnt': 'sum'
})
Selisih = selisih(result['cnt'].to_list())
selisih_df = pd.DataFrame(Selisih, columns=['selisih'])
month_selisih = ['January-Februari','Februari-Maret','Maret-April','April-Mei',
                 'Mei-Juni','Juni-Juli','Juli-Agustus','Agustus-September',
                 'September-Oktober','Oktober-November','November-Desember']
selisih_df['Bulan'] = month_selisih
selisih_df['Persentase'] = round(selisih_df['selisih'] / result['cnt'].sum() * 100,2)
selisih_df['Persentase'] = selisih_df['Persentase'].apply(lambda x: f'{x:.2f}%')
st.write(selisih_df)

### Langkah Penyelesaian

if st.button('Tampilkan Langkah Penyelesaian No. 2') :
    
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(['Langkah 1','Langkah 2','Langkah 3','Langkah 4',
                                             'Langkah 5','Langkah 6'])
     
    with tab1:
        code = """
        day_df = day_df[day_df['yr'] == 1]
        """
        st.code(code, language='python')
        st.write("""
                Melakukan filtering untuk mendapatkan data yang dihasilkan pada tahun 2012.
                """)
    with tab2:
        code = """
        def selisih(x):
            lst = []
            for i in range(len(x)-1):
                if x[i] > x[i+1]:
                    c = (x[i] - x[i+1]) * -1
                    lst.append(c)
                elif x[i] < x[i+1]:
                    c = x[i+1] - x[i]
                    lst.append(c)
            return lst
        """
        st.code(code,language='python')
        st.write("""
                Membuat fungsi untuk menghitung selisih jumlah pengguna sepeda tiap bulannya.               
                """)
    with tab3:
        code = """
        result = day_df.groupby(by='mnth').agg({
                'cnt': 'sum'
                })        
        """
        st.code(code, language='python')
        st.write("""
                Membuat pivot table yang didasarkan pada bulan ('mnth') dan memiliki value 
                jumlah dari kolom 'cnt'.               
                """)
    with tab4:
        code = """
        Selisih = selisih(result['cnt'].to_list())
        """
        st.code(code, language='python')
        st.write("""
                Menghitung selisih jumlah penyewa tiap bulan dengan format list yang nantinya 
                akan dimasukkan kedalam dataframe baru.
                """)
    with tab5:
        code = """
        selisih_df = pd.DataFrame(Selisih, columns=['selisih'])
        month_selisih = ['January-Februari','Februari-Maret','Maret-April','April-Mei',
                         'Mei-Juni','Juni-Juli','Juli-Agustus','Agustus-September',
                         'September-Oktober','Oktober-November','November-Desember']
        selisih_df['Bulan'] = month_selisih
        """
        st.code(code, language='python')
        st.write("""
                Menciptakan sebuah dataframe baru yang berisi kolom selisih dan periode bulannya.
                """)
    with tab6:
        code = """
        selisih_df['Persentase'] = round(selisih_df['selisih'] / result['cnt'].sum() * 100,2)
        selisih_df['Persentase'] = selisih_df['Persentase'].apply(lambda x: f'{x:.2f}%')
        """
        st.code(code, language='python')
        st.write("""
                Membuat kolom baru yang berisikan persentase kenaikan atau penurunannya 
                (selisih dibagi dengan jumlah total penyewa di tahun 2012 kemudian dikali 100).
                """)

### Data Visualization
st.write("### Visualisasi Data")

st.header("Kenaikan dan Penurunan Jumlah Penyewa Sepeda Tahun 2012")
months = ['January','Februari','Maret','April','Mei','Juni','Juli',
            'Agustus','September','Oktober','November','Desember']
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(result.index, result['cnt'])
ax.grid(True)
ax.set_title('Data Jumlah Penyewa Tiap Bulan')
ax.set_xticks(np.arange(1,13,1),months)
st.pyplot(fig)

### Result

st.write('#### Hasil Analisis')

col1,col2 = st.columns([1,1])

with col1 :
    st.header('Kenaikan Tertinggi')
    naik_max = selisih_df[(selisih_df['selisih'] == selisih_df['selisih'].max())]
    st.write(naik_max)
with col2 :
    st.header('Penurunan Tertinggi')
    turun_max = selisih_df[(selisih_df['selisih'] == selisih_df['selisih'].min())]
    st.write(turun_max)

### Conclusion

with st.expander('Kesimpulan'):
        st.write("""
                Berdasarkan analisis data yang dilakukan terhadap dataset day.csv, ditemukan kesimpulan 
                mengenai bagaimana kenaikan dan penurunan jumlah penyewa sepeda pada tahun 2012.

                Kesimpulan pertama, didapatkan data bahwa jumlah penyewa sepeda pada tahun 2012 mengalami 
                peningkatan selama bulan Januari sampai dengan bulan September. Sedangkan penurunan jumlah 
                penyewa terjadi selama bulan September sampai dengan bulan Desember.

                Kesimpulan kedua, ditemukan data bahwa kenaikan jumlah penyewa tertinggi terjadi pada 
                periode bulan Februari-Maret dengan kenaikan sebanyak 61.738 penyewa atau peningkatan 
                sebanyak 3,01 %. Sedangkan penurunan jumlah penyewa tertinggi terjadi pada periode bulan 
                Oktober-November dengan penurunan sebanyak 46.177 penyewa atau penurunan sebanyak 2,25 %.                
                """)
