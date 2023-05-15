"""Module providingFunction printing
python version."""
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


pd.options.mode.chained_assignment = \
    None

# Read data from Excel file
df311 = pd.read_excel('Podatki_Podravje_temp_postaja_311.xlsx')
df311['datum'] = pd.to_datetime(df311['datum'])
df311 = df311[~(df311['datum'] < '2012-01-01')]
df311 = df311.reset_index(drop=True)

df311['90th_centile'] = np.nan

for i, row in df311.iterrows():
    datum = row['datum']
    max_temp = row['tmax']

    zac_datum = datum - pd.Timedelta(
        days=15)
    kon_datum = datum + pd.Timedelta(
        days=15)
    temp_data = df311.loc[(df311[
                               'datum'] >= zac_datum) & (
                                  df311[
                                      'datum'] <= kon_datum), 'tmax']

    percentile = np.percentile(
        temp_data, 90)
    df311.at[
        i, '90th_centile'] = percentile

    p25 = np.percentile(temp_data, 25)
    df311.at[i, '25th_centile'] = p25
    p75 = np.percentile(temp_data, 75)
    df311.at[i, '75th_centile'] = p75

# Create boolean column for
# consecutive days above 90th percentile
pogoj = df311['tmax'] > df311[
    '90th_centile']
df311['dan_prek_90_centil'] = [
                                        False] * \
                                    df311.shape[
                                        0]
df311['dan_prek_90_centil'][
    pogoj] = True

# Create boolean column for heat waves
df311['vrocinski_val'] = df311[
                             'dan_prek_90_centil'] & \
                         df311[
                             'dan_prek_90_centil'].shift(
                             1) & \
                         df311[
                             'dan_prek_90_centil'].shift(
                             2)
df311['vrocinski_val'] |= df311[
                              'vrocinski_val'].shift(
    -1) | df311['vrocinski_val'].shift(
    -2)
df311['vrocinski_val'] = df311[
    'vrocinski_val'].fillna(False)


def align_center(j):
    """
    Function to align text in the
    center for pandas DataFrame styles.

    Args:
        j (str): Style string.

    Returns:
        str: Style string with center
        alignment.
    """
    return ['text-align: center' for _
            in j]


# Copy a subset of columns from df311
# DataFrame
df_vrocinski_val = df311[
    ['datum', 'vrocinski_val']].copy()
# Create a writer for Excel file
writer = pd.ExcelWriter(
    "vrocinski_val.xlsx",
    engine="xlsxwriter",
    date_format="dd/mm/yyyy",
    datetime_format="dd/mm/yyyy")
# Apply style to the df_vrocinski_val
# DataFrame and write it to Excel sheet
df_vrocinski_val.style.apply(align_center,
                        axis=0).to_excel(
    writer, sheet_name="vroc_val")
# Get the workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets["vroc_val"]
# Set column width for the worksheet
(max_row, max_col) = df_vrocinski_val.shape
worksheet.set_column(1, max_col, 20)
# Close the writer
writer.close()

# Count occurrences of True values in
# 'vrocinski_val' column
STEVEC = 0
for x in df311['vrocinski_val']:
    if x:
        STEVEC += 1

my_list = []

# Calculate values for 'my_list'
# based on 'tmax' column values and
# 'p25' and 'p75' variables
for i in range(df311.shape[0]):
    if df311.at[i, 'tmax'] > p25:
        my_list.append((df311.at[
                            i,
                            'tmax'] -
                        p25) / (
                               p75 -
                               p25))
    else:
        my_list.append(0)


# Read data from an Excel file
df = pd.read_excel(
    'Podaki o umrlih_po vzroku, '
    'datumu smrti, obcini in statusu '
    'aktivnosti_2012-2021.xlsx',
    sheet_name="Tabela"
)

# Delete rows, where date is after 2021-01-01
df = df[df['Datum smrti'] < pd.Timestamp('2021-01-01')]

# Rename the columns
new_column_names = {
    "vzroksmrti -združene kategorije": "vzrok",
    "obcina prebivalisca": "obcina",
    "status aktivnosti": "aktivnost"
}
df = df.rename(columns=new_column_names)


seznam_obcin = df['obcina'].dropna().unique().tolist()
seznam_obcin.sort()
seznam_vzrokov = df['vzrok'].dropna().unique().tolist()
seznam_vzrokov.sort()
seznam_aktivnosti = df['aktivnost'].dropna().unique().tolist()
seznam_aktivnosti.sort()


def t_test(df, tip, kategorija, df_vrocinski_val):
    """
        Performs a t-test for two samples
        on the 'Count' column of the
        merged data frame for a given
        category.

        Args:
            df (pd.DataFrame):
            Data frame containing the
            data of occurred deaths.
            tip (str): type of category.
            kategorija (str): category.
            df_vrocinski_val (pd.DataFrame):
            Data frame containing the
            data of heat waves.

        Returns:
            tuple: A tuple containing the
            p-value and the total count
            of deaths for the category.

        Description:
            This function performs a
            t-test for two samples on the
            'Count' column of the merged
            data frame for a given
            category.
            It calculates the total count
            of deaths and performs a t-test.
        """

    df_kategorije = df[df[tip] == kategorija]
    tmp1 = df_kategorije.groupby(
        "Datum smrti").size().values
    df_kategorije = \
        df_kategorije.drop_duplicates(
            subset="Datum "
                   "smrti").assign(
            Count=tmp1)
    df_kategorije.loc[df[
                      'število ' \
                      'umrlih'] == 0,
    'Count'] = 0
    df_kategorije = df_kategorije.drop(
        columns=['Leto',"obcina", "vzrok", "aktivnost",
                 'število umrlih'])

    df_kategorije = df_kategorije.rename(
        columns={
            'Datum smrti': 'datum'})

    merged_df = pd.merge(df_vrocinski_val,
                         df_kategorije,
                         on='datum',
                         how='outer')
    merged_df["Count"] = merged_df[
        "Count"].fillna(0)
    stevilo_pojavitev_smrti = \
        merged_df['Count'].sum()

    df_je_vrocinski_val = merged_df[
        merged_df[
            'vrocinski_val'] == True]
    df_ni_vrocinski_val = merged_df[
        merged_df[
            'vrocinski_val'] == False]

    _, p_value = ttest_ind(
        df_je_vrocinski_val['Count'],
        df_ni_vrocinski_val['Count'])

    return p_value, \
        stevilo_pojavitev_smrti


def analiza(df, tip, stolpec_s_kategorijami, df_vrocinski_val):
    """
        Performs a t-test for two samples on the 'Count' column
        of the merged data frame for all categories of type tip.

        Args:
            df (pd.DataFrame): Data frame containing the data
            of occurred deaths.
            tip (str): The name of the category.
            stolpec_s_kategorijami (list): A list of all
            categories of type tip.
            df_vrocinski_val (pd.DataFrame): Data frame containing
            the data of heat waves.

        Returns:
            None

        Description:
            This function performs a t-test for two samples on the
            'Count' column of the merged data frame for all
            categories of type tip. It calculates the p-value and
            the total count of deaths for each category in the list
            of categories. The results are stored in a new data
            frame and saved as an Excel file.
    """

    df_rezultat = pd.DataFrame(stolpec_s_kategorijami,
                             columns=[
                                 tip])

    for kategorija in stolpec_s_kategorijami:
        p_vrednost, stevilo_pojavitev_smrti = \
            t_test(df, tip, kategorija, df_vrocinski_val)

        df_rezultat.loc[df_rezultat[tip] == kategorija,\
            'p_vrednost'] = p_vrednost
        df_rezultat.loc[df_rezultat[tip] == kategorija,\
            'stevilo_pojavitev_smrti'] = \
            int(stevilo_pojavitev_smrti)

    with pd.ExcelWriter(
            tip+
            '.xlsx',
            engine='xlsxwriter',
            engine_kwargs={'options': {
                'strings_to_numbers':
                    True}}) as writer:
        df_rezultat.to_excel(
            writer)


tip = ["obcina", "vzrok", "aktivnost"]
seznam_seznamov = [seznam_obcin, seznam_vzrokov, seznam_aktivnosti]
slovar_seznamov = dict(zip(tip, seznam_seznamov))

for tip, seznam in slovar_seznamov.items():
    analiza(df, tip, seznam, df_vrocinski_val)