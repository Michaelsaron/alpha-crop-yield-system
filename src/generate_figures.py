from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.base import clone
import joblib, json

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
train=pd.read_csv(ROOT/'data/processed/master_train.csv')
weather=pd.read_csv(ROOT/'data/processed/clean_weather.csv')
prices=pd.read_csv(ROOT/'data/processed/clean_prices.csv')
raw_train=pd.read_csv(ROOT/'data/raw/crop_yield_train.csv')
raw_weather=pd.read_csv(ROOT/'data/raw/regional_weather.csv')
raw_prices=pd.read_csv(ROOT/'data/raw/market_prices.csv')
model=joblib.load(ROOT/'models/final_model.joblib')
meta=json.loads((ROOT/'models/model_metadata.json').read_text())

plt.rcParams.update({'font.size':11,'axes.titlesize':15,'axes.labelsize':12,'legend.fontsize':10,'figure.titlesize':16})
COLORS=['#0072B2','#E69F00','#009E73','#CC79A7','#56B4E9','#D55E00','#F0E442','#000000']

def save(fig,name):
    fig.tight_layout(); fig.savefig(FIG/name,dpi=180,bbox_inches='tight'); plt.close(fig)

def invalid_rate(df):
    return ((df.isna()) | (df.eq(-999) if True else False)).mean()*100
# 1
parts=[]
for label,d in [('plot',raw_train),('weather',raw_weather),('price',raw_prices)]:
    r=invalid_rate(d); parts.append(pd.DataFrame({'column':[f'{label}: {c}' for c in r.index],'pct':r.values}))
z=pd.concat(parts).sort_values('pct',ascending=True)
fig,ax=plt.subplots(figsize=(12,8)); ax.barh(z.column,z.pct,color=COLORS[0]); ax.set(title='Missing or Invalid Values in Raw Tables',xlabel='Missing or -999 values (%)',ylabel='Column'); ax.set_xlim(left=0); ax.grid(axis='x',alpha=.2); save(fig,'fig01_missingness.png')
# 2 price and labor before/after
fig,axs=plt.subplots(1,2,figsize=(13,5))
rawp=pd.to_numeric(raw_prices['price_birr_per_quintal'],errors='coerce'); cleanp=prices['price_birr_per_quintal']
axs[0].hist(rawp.dropna(),bins=25,alpha=.55,label='Raw',color=COLORS[1]); axs[0].hist(cleanp.dropna(),bins=25,alpha=.55,label='Cleaned',color=COLORS[0]); axs[0].set(title='Price Before vs After Cleaning',xlabel='Price (birr/quintal)',ylabel='Rows'); axs[0].legend()
rawl=pd.to_numeric(raw_train['labor_days_per_ha'],errors='coerce').replace(-999,np.nan); cleanl=train['labor_days_per_ha']
axs[1].hist(rawl.dropna(),bins=25,alpha=.55,label='Raw valid values',color=COLORS[1]); axs[1].hist(cleanl.dropna(),bins=25,alpha=.55,label='Cleaned / imputed',color=COLORS[0]); axs[1].set(title='Labor Before vs After Cleaning',xlabel='Labor (days/ha)',ylabel='Plots'); axs[1].legend(); save(fig,'fig02_before_after_cleaning.png')
# 3
fig,ax=plt.subplots(figsize=(11,6)); crops=sorted(train.crop_type.unique())
for i,c in enumerate(crops): ax.hist(train.loc[train.crop_type==c,'yield_tons_per_ha'],bins=28,histtype='step',linewidth=2,label=c,color=COLORS[i])
ax.set(title='Yield Distribution by Crop',xlabel='Yield (tons/ha)',ylabel='Plots'); ax.legend(title='Crop'); ax.set_xlim(left=0); save(fig,'fig03_yield_distribution.png')
# 4
piv=train.pivot_table(index='region',columns='crop_type',values='yield_tons_per_ha',aggfunc='mean'); cnt=train.pivot_table(index='region',columns='crop_type',values='yield_tons_per_ha',aggfunc='size')
fig,ax=plt.subplots(figsize=(10,6)); im=ax.imshow(piv.values,aspect='auto',cmap='viridis'); ax.set_xticks(range(len(piv.columns)),piv.columns); ax.set_yticks(range(len(piv.index)),piv.index); ax.set(title='Mean Yield by Region and Crop',xlabel='Crop type',ylabel='Region')
for i in range(piv.shape[0]):
 for j in range(piv.shape[1]): ax.text(j,i,f'{piv.iloc[i,j]:.2f}\n(n={cnt.iloc[i,j]:.0f})',ha='center',va='center',color='white' if piv.iloc[i,j]<piv.values.mean() else 'black',fontsize=9)
cbar=fig.colorbar(im,ax=ax); cbar.set_label('Mean yield (tons/ha)'); save(fig,'fig04_region_crop_heatmap.png')
#5
cols=['yield_tons_per_ha','altitude_m','rainfall_mm_season','farm_size_ha','fertilizer_kg_per_ha','soil_quality_index','labor_days_per_ha','distance_to_market_km','season_avg_temp_c','season_rainfall_mm','season_extreme_heat_days','season_temp_deviation_c']
corr=train[cols].corr(); fig,ax=plt.subplots(figsize=(12,9)); im=ax.imshow(corr.values,vmin=-1,vmax=1,cmap='coolwarm'); ax.set_xticks(range(len(cols)),cols,rotation=60,ha='right'); ax.set_yticks(range(len(cols)),cols); ax.set(title='Correlation of Yield, Plot and Weather Features',xlabel='Feature',ylabel='Feature'); cbar=fig.colorbar(im,ax=ax); cbar.set_label('Pearson correlation'); save(fig,'fig05_correlation_heatmap.png')
#6
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; mm={m:i for i,m in enumerate(months)}; w=weather.copy(); w['m']=w.month.map(mm); g=w.groupby(['region','m']).avg_temp_c.mean().reset_index()
fig,ax=plt.subplots(figsize=(11,6));
for i,(r,gg) in enumerate(g.groupby('region')): ax.plot(gg.m,gg.avg_temp_c,marker='o',label=r,color=COLORS[i])
ax.axvspan(5,8,alpha=.10,color='grey',label='Example Jun–Sep growing window'); ax.set_xticks(range(12),months); ax.set(title='Monthly Average Temperature by Region',xlabel='Month',ylabel='Average temperature (°C)'); ax.legend(ncol=2); save(fig,'fig06_climate_by_region.png')
#7
fig,ax=plt.subplots(figsize=(11,6))
for i,c in enumerate(crops):
 d=train[train.crop_type==c].copy(); d['bin']=pd.qcut(d.season_avg_temp_c,6,duplicates='drop'); q=d.groupby('bin',observed=True).agg(temp=('season_avg_temp_c','mean'),y=('yield_tons_per_ha','mean')); ax.plot(q.temp,q.y,marker='o',label=c,color=COLORS[i])
ax.set(title='Yield Response to Growing-Season Temperature',xlabel='Season average temperature (°C)',ylabel='Mean yield (tons/ha)'); ax.legend(title='Crop'); ax.set_ylim(bottom=0); save(fig,'fig07_yield_vs_season_temp.png')
#8
pg=prices.groupby(['year','crop_type']).price_birr_per_quintal.mean().reset_index(); fig,ax=plt.subplots(figsize=(11,6))
for i,c in enumerate(crops):
 d=pg[pg.crop_type==c]; ax.plot(d.year,d.price_birr_per_quintal,marker='o',label=c,color=COLORS[i])
ax.set_xticks(sorted(pg.year.unique())); ax.set(title='Average Crop Price Trends, 2021–2024',xlabel='Year',ylabel='Price (birr/quintal)'); ax.legend(title='Crop'); ax.set_ylim(bottom=0); save(fig,'fig08_price_trends.png')
#9
rv=train.assign(revenue_ha=train.yield_tons_per_ha*10*train.price_birr_per_quintal).groupby(['region','crop_type']).revenue_ha.mean().unstack(); fig,ax=plt.subplots(figsize=(12,6)); x=np.arange(len(rv.index)); width=.15
for j,c in enumerate(rv.columns): ax.bar(x+(j-2)*width,rv[c],width,label=c,color=COLORS[j])
ax.set_xticks(x,rv.index); ax.set(title='Estimated Revenue per Hectare by Region and Crop',xlabel='Region',ylabel='Estimated revenue (birr/ha)'); ax.legend(title='Crop',ncol=5); ax.set_ylim(bottom=0); save(fig,'fig09_revenue_by_crop_region.png')
#10
mc=pd.read_csv(ROOT/'reports/model_comparison.csv'); fig,ax=plt.subplots(figsize=(10,6)); bars=ax.bar(mc.model,mc.RMSE,color=[COLORS[0] if m=='LightGBM' else COLORS[4] for m in mc.model]);
idx=mc.index[mc.model=='LightGBM'][0]; ax.errorbar(idx,mc.loc[idx,'RMSE'],yerr=meta['cv_rmse_std'],fmt='none',ecolor='black',capsize=5,label='LightGBM 5-fold CV ±1 SD'); base=float(mc.loc[mc.model.str.contains('Mean'),'RMSE'].iloc[0]); ax.axhline(base,linestyle='--',color='black',label=f'Mean baseline RMSE = {base:.2f}'); ax.set(title='Validation RMSE by Model',xlabel='Model',ylabel='RMSE (tons/ha)'); ax.tick_params(axis='x',rotation=20); ax.legend(); ax.set_ylim(bottom=0); save(fig,'fig10_model_comparison.png')
#11 honest held-out refit using final pipeline structure
X=train[meta['features']]; y=train.yield_tons_per_ha; Xtr,Xv,ytr,yv=train_test_split(X,y,test_size=.2,random_state=42); m=clone(model); m.fit(Xtr,ytr); pr=m.predict(Xv); res=yv-pr
fig,axs=plt.subplots(1,2,figsize=(13,5)); axs[0].scatter(yv,pr,s=12,alpha=.35,color=COLORS[0],label='Validation plots'); lo=min(yv.min(),pr.min()); hi=max(yv.max(),pr.max()); axs[0].plot([lo,hi],[lo,hi],'--',color='black',label='Perfect prediction (y=x)'); axs[0].set(title='Predicted vs Actual Yield',xlabel='Actual yield (tons/ha)',ylabel='Predicted yield (tons/ha)'); axs[0].legend(); axs[1].scatter(pr,res,s=12,alpha=.35,color=COLORS[1],label='Residuals'); axs[1].axhline(0,linestyle='--',color='black',label='Zero error'); axs[1].set(title='Residuals vs Predicted Yield',xlabel='Predicted yield (tons/ha)',ylabel='Residual = actual − predicted (tons/ha)'); axs[1].legend(); save(fig,'fig11_predicted_vs_actual_residuals.png')
#12 permutation importance on holdout
from sklearn.inspection import permutation_importance
pi=permutation_importance(m,Xv,yv,n_repeats=3,random_state=42,scoring='neg_root_mean_squared_error',n_jobs=-1); imp=pd.Series(pi.importances_mean,index=meta['features']).sort_values(ascending=False).head(12).sort_values(); weather_feats={'season_avg_temp_c','season_rainfall_mm','season_extreme_heat_days','season_temp_deviation_c','rainfall_gap_mm'}; colors=[COLORS[1] if f in weather_feats else COLORS[0] for f in imp.index]
fig,ax=plt.subplots(figsize=(11,7)); ax.barh(imp.index,imp.values,color=colors); from matplotlib.patches import Patch; ax.legend(handles=[Patch(color=COLORS[1],label='Weather-derived'),Patch(color=COLORS[0],label='Other feature')]); ax.set(title='Permutation Importance of Final Model Features',xlabel='Increase in RMSE when shuffled (tons/ha)',ylabel='Feature'); ax.set_xlim(left=0); save(fig,'fig12_feature_importance.png')
print('Generated 12 figures in',FIG)
