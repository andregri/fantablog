To download "classifica":
```bash
for i in {1..20}; do
curl "https://leghe.fantacalcio.it/servizi/V1_LegheCompetizione/ClassificaGiornate?alias_lega=cempions-lug&id_competizione=215917&giornata_inizio=1&giornata_fine=${i}&_=1706354752948" ... | jq . > classifica_${i}.json
done
```

To download "giornata":
```bash
for i in {1..20}; do
curl "https://leghe.fantacalcio.it/servizi/V1_LegheFormazioni/Pagina?id_comp=215917&r=${i}&f=${i}_1696312019927.json" ... | jq . > giornata${i}.json
done
```