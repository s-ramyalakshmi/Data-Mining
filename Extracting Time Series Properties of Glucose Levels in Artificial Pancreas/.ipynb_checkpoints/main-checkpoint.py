{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "e813583a",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "92f5ab95",
   "metadata": {},
   "outputs": [],
   "source": [
    "cgm = pd.read_csv('/Users/ramya/Documents/Python/Project/CGMData.csv',low_memory=False, usecols=['Date','Time','Sensor Glucose (mg/dL)'])\n",
    "insulin = pd.read_csv('/Users/ramya/Documents/Python/Project/InsulinData.csv', low_memory=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "f14d300e",
   "metadata": {},
   "outputs": [],
   "source": [
    "cgm['date_time'] = pd.to_datetime(cgm['Date'] + ' ' + cgm['Time'])\n",
    "cgm = cgm.set_index('Date').drop(index=cgm[cgm['Sensor Glucose (mg/dL)'].isna()]['Date'].unique()).reset_index()\n",
    "cgm_data_test = cgm.copy().set_index(pd.DatetimeIndex(cgm['date_time']))\n",
    "\n",
    "insulin['date_time'] = pd.to_datetime(insulin['Date'] + ' ' + insulin['Time'])\n",
    "\n",
    "auto_mode_start = insulin.sort_values(by='date_time',ascending=True).loc[insulin['Alarm']=='AUTO MODE ACTIVE PLGM OFF'].iloc[0]['date_time']\n",
    "auto_mode_df=cgm.sort_values(by='date_time',ascending=True).loc[cgm['date_time'] >= auto_mode_start]\n",
    "\n",
    "manual_mode_df = cgm.sort_values(by='date_time',ascending=True).loc[cgm['date_time'] < auto_mode_start]\n",
    "auto_mode_df_date_index=auto_mode_df.copy().set_index('date_time')\n",
    "\n",
    "li1=auto_mode_df_date_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.8*288).dropna().index.tolist()\n",
    "auto_mode_df_date_index=auto_mode_df_date_index.loc[auto_mode_df_date_index['Date'].isin(li1)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "df8aef1c",
   "metadata": {},
   "outputs": [],
   "source": [
    "percent_hyperglycemia_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_df_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_df_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_wholeday_automode=(auto_mode_df_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_daytime_automode=(auto_mode_df_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_overnight_automode=(auto_mode_df_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_df_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "c4e9006d",
   "metadata": {},
   "outputs": [],
   "source": [
    "manual_mode_df_index = manual_mode_df.copy().set_index('date_time')\n",
    "\n",
    "li2 = manual_mode_df_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.8*288).dropna().index.tolist()\n",
    "manual_mode_df_index=manual_mode_df_index.loc[manual_mode_df_index['Date'].isin(li2)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "b27aa265",
   "metadata": {},
   "outputs": [],
   "source": [
    "percent_hyperglycemia_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hyperglycemia_critical_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_range_sec_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_df_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_df_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv1_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_wholeday_manual=(manual_mode_df_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_daytime_manual=(manual_mode_df_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)\n",
    "\n",
    "percent_hypoglycemia_lv2_overnight_manual=(manual_mode_df_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_df_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "2f9380ea",
   "metadata": {},
   "outputs": [],
   "source": [
    "res_df = pd.DataFrame({'percent_hyperglycemia_overnight':[ percent_hyperglycemia_overnight_manual.mean(axis=0),percent_hyperglycemia_overnight_automode.mean(axis=0)],\n",
    "\n",
    "\n",
    "'percent_hyperglycemia_critical_overnight':[ percent_hyperglycemia_critical_overnight_manual.mean(axis=0),percent_hyperglycemia_critical_overnight_automode.mean(axis=0)],\n",
    "\n",
    "\n",
    "'percent_range_overnight':[ percent_range_overnight_manual.mean(axis=0),percent_range_overnight_automode.mean(axis=0)],\n",
    "\n",
    "\n",
    "'percent_range_sec_overnight':[ percent_range_sec_overnight_manual.mean(axis=0),percent_range_sec_overnight_automode.mean(axis=0)],\n",
    "\n",
    "\n",
    "'percent_hypoglycemia_lv1_overnight':[ percent_hypoglycemia_lv1_overnight_manual.mean(axis=0),percent_hypoglycemia_lv1_overnight_automode.mean(axis=0)],\n",
    "\n",
    "\n",
    "'percent_hypoglycemia_lv2_overnight':[ np.nan_to_num(percent_hypoglycemia_lv2_overnight_manual.mean(axis=0)),percent_hypoglycemia_lv2_overnight_automode.mean(axis=0)],\n",
    "                           'percent_hyperglycemia_daytime':[ percent_hyperglycemia_daytime_manual.mean(axis=0),percent_hyperglycemia_daytime_automode.mean(axis=0)],\n",
    "                           'percent_hyperglycemia_critical_daytime':[ percent_hyperglycemia_critical_daytime_manual.mean(axis=0),percent_hyperglycemia_critical_daytime_automode.mean(axis=0)],\n",
    "                           'percent_range_daytime':[ percent_range_daytime_manual.mean(axis=0),percent_range_daytime_automode.mean(axis=0)],\n",
    "                           'percent_range_sec_daytime':[ percent_range_sec_daytime_manual.mean(axis=0),percent_range_sec_daytime_automode.mean(axis=0)],\n",
    "                           'percent_hypoglycemia_lv1_daytime':[ percent_hypoglycemia_lv1_daytime_manual.mean(axis=0),percent_hypoglycemia_lv1_daytime_automode.mean(axis=0)],\n",
    "                           'percent_hypoglycemia_lv2_daytime':[ percent_hypoglycemia_lv2_daytime_manual.mean(axis=0),percent_hypoglycemia_lv2_daytime_automode.mean(axis=0)],    \n",
    "                           'percent_hyperglycemia_wholeday':[ percent_hyperglycemia_wholeday_manual.mean(axis=0),percent_hyperglycemia_wholeday_automode.mean(axis=0)],\n",
    "                           'percent_hyperglycemia_critical_wholeday':[ percent_hyperglycemia_critical_wholeday_manual.mean(axis=0),percent_hyperglycemia_critical_wholeday_automode.mean(axis=0)],\n",
    "                           'percent_range_wholeday':[ percent_range_wholeday_manual.mean(axis=0),percent_range_wholeday_automode.mean(axis=0)],\n",
    "                           'percent_range_sec_wholeday':[ percent_range_sec_wholeday_manual.mean(axis=0),percent_range_sec_wholeday_automode.mean(axis=0)],\n",
    "                           'percent_hypoglycemia_lv1_wholeday':[ percent_hypoglycemia_lv1_wholeday_manual.mean(axis=0),percent_hypoglycemia_lv1_wholeday_automode.mean(axis=0)],\n",
    "                           'percent_hypoglycemia_lv2_wholeday':[ percent_hypoglycemia_lv2_wholeday_manual.mean(axis=0),percent_hypoglycemia_lv2_wholeday_automode.mean(axis=0)]},\n",
    "                          index=['manual_mode','auto_mode'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "7a4c8b2e",
   "metadata": {},
   "outputs": [],
   "source": [
    "res_df.to_csv('/Users/ramya/Documents/Python/Project/Results.csv',header=False,index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bb86645a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
