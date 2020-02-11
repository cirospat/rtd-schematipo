
# 3 - messaggi_colorati.md


<div class="alert alert-primary" role="alert">
This is a primary alert—check it out!
</div>

---


<div class="alert alert-secondary" role="alert">
  This is a secondary alert—check it out!
</div>

---

```html
<div class="alert alert-success" role="alert">
  This is a success alert—check it out!
</div>
```


```html
<div class="alert alert-danger" role="alert">
  This is a danger alert—check it out!
</div>
```

```html
<div class="alert alert-warning" role="alert">
  This is a warning alert—check it out!
</div>
```

```html
<div class="alert alert-info" role="alert">
  This is a info alert—check it out!
</div>
```

```html
<div class="alert alert-light" role="alert">
  This is a light alert—check it out!
</div>
```

```html
<div class="alert alert-dark" role="alert">
  This is a dark alert—check it out!
</div>
```

---

## Esempio di tabella

CARATTERE|SIGNIFICATO|ESEMPIO
---------|-----------|------
`*` | corrisponde a **zero**, **uno** o **più** del carattere precedente | `Ah*` corrisponde a `Ahhhhh` o `A`
`?` | corrisponde a zero o uno del carattere precedente |	`Ah?` corrisponde a `A` o `Ah`
`+` | corrisponde a **uno** o **più** del carattere precedente  |	`Ah+` corrisponde a `Ah` o `Ahhh` ma non a  `A`
`\` | Usato per escludere un carattere speciale | `Hungry\?` corrisponde a `Hungry?`
`.` | Wildcard, carattere jolly, corrisponde a **qualsiasi** carattere |	`do.*` corrisponde a `dog`, `door`, `dot`, etc.
`( )` | **Gruppo** di caratteri	Vedi ad esempio `|`
`[ ]` | corrisponde ad un **range** di caratteri | `[cbf]ar` corrisponde a `car`, `bar`, o `far`; `[0-9]+` corrisponde a **qualsiasi** numero intero positivo tra 0 e 9 inclusi; `[a-zA-Z]` corrisponde a lettere ASCII `a-z` (maiuscole e minuscole); `[^0-9]` corrisponde a **qualsiasi** carattere non numerico
`|` | corrisponde al precedente OR successivo carattere/gruppo |	`(Mon)|(Tues)day` corrisponde a `Monday` o `Tuesday`
`{ }` | corrisponde aa un numero specificato di occorrenze del carattere precedente | `[0-9]{3}` corrisponde a `315` ma non a  `31`; `[0-9]{2,4}` corrisponde a `18`, `125` e  `1234`; `[0-9]{2,}` corrisponde a `1234567…`
`^` | Inizio di una stringa o all'interno di un intervallo di caratteri [] negazione.	| `^http` corrisponde stringhe che iniziano con `http`, ad esempio un URL. `[^0-9]` corrisponde a qualsiasi carattere diverso da `0-9`.
`$` | Fine stringa | `ta$` corrisponde a `cascata` e no a `tavola`

---
 
## Esempio di video incorporato su file `.MD` 
 
<iframe width="100%" height="500" src="https://www.youtube.com/embed/Zj2Kosq-v6k" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
<span class="footer_small">Raduno della community di OpendataSicilia del 9 e 10 novembre 2018 a Palermo.</span>

---


<table cellspacing="0" cellpadding="0" style="width:96%">
    <thead>
    <tr><th style="text-align:center;width:71%;color:#0c0c0f;vertical-align:Top;padding-top:11px;padding-bottom:11px;padding-left:11px;padding-right:11px;border:solid 0.5px #666666"><p style="color:#0c0c0f;font-family:Verdana"><span  style="color:#0c0c0f;font-family:Verdana">Adempimento</span></p></th><th style="text-align:center;width:29%;color:#0c0c0f;vertical-align:Top;padding-top:11px;padding-bottom:11px;padding-left:11px;padding-right:11px;border:solid 0.5px #666666"><p style="color:#0c0c0f;font-family:Verdana"><span  style="color:#0c0c0f;font-family:Verdana">Capo, articolo</span></p></th></tr>
    </thead><tbody>
    <tr><td style="background-color:#00ffff;color:#0c0c0f;vertical-align:Top;padding-top:11px;padding-bottom:11px;padding-left:11px;padding-right:11px;border:solid 0.5px #666666"><p style="background-color:#00ffff;color:#0c0c0f;font-family:Verdana;margin-bottom:15"><span  style="background-color:#00ffff;color:#0c0c0f;font-family:Verdana">Si tratta di adempimenti volontari del titolare mediante i quali può implementare importanti misure di sicurezza dei trattamenti e dimostrare la conformità delle attività di trattamento ai requisiti stabiliti dal Regolamento.</span></p></td><td style="text-align:center;vertical-align:Top;padding-top:11px;padding-bottom:11px;padding-left:11px;padding-right:11px;border:solid 0.5px #666666"><p style="font-family:Verdana;margin-bottom:15"><span  style="font-family:Verdana"><span style="font-weight:bold">IV, </span><a href="http://www.altalex.com/documents/leggi/2018/03/05/titolare-e-responsabile-del-trattamento-gdpr#art40" target="_blank">40-42</a></span></p></td></tr>
    </tbody></table>
