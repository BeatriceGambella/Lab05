import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    #campi da inserire per aggiungere un nuovo strumento al deposito
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno acquisto")

    # TextField del contatore per il valore in euro
    input_prezzo = ft.TextField(
        value="0.00",                   #imposta valore iniziale del contatore
        width=100,                      #imposta la larghezza del riquadro in cui è contenuto il prezzo
        disabled=True,                  #disabilità la possibilità di inserire il prezzo da tastiera
        text_align=ft.TextAlign.CENTER            #allinea il prezzo all'interno del riquadro
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    #handler per aumentare il prezzo nel contatore quando si preme l'icona "+"
    def incrementa_prezzo():
        prezzo = float(input_prezzo.value)              #trasforma la stringa del prezzo in un float
        input_prezzo.value = f"{prezzo + 1:.2f}"        #incrementa di uno il prezzo
        input_prezzo.update()                           #aggiorna il prezzo

    # handler per diminuire il prezzo nel contatore quando si preme l'icona "-"
    def decrementa_prezzo():
        prezzo = float(input_prezzo.value)              #trasforma la stringa del prezzo in un float
        if prezzo>0:                                    #controlla che il prezzo non diventi negativo
            input_prezzo.value = f"{prezzo - 1:.2f}"    #decrementa di uno il prezzo
            input_prezzo.update()                       #aggiorna il prezzo

    #handler per aggiungere un nuovo strumento al deposito
    def aggiungi_strumento():
        try:
            deposito.aggiungi_strumento(                 #viene aggiunto uno strumento al deposito attraverso il metodo
                input_tipo.value,                        #aggiungi strumento passando come parametri i valori dei
                input_marca.value,                       #TextField dello strumento
                int(input_anno.value),
                float(input_prezzo.value)
            )
            input_tipo.value = input_marca.value = input_anno.value = ""        #i vari campi vengono ripristinati
            input_prezzo.value = "0.00"                                         #a prima che venissero compilati
            aggiorna_lista_strumenti()                  # viene chiamata la funzione che aggiorna la lista strumenti
        #se nei campi anno e prezzo vengono inseriti dei valori che non sono numeri viene scatenato un errore
        except ValueError:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e prezzo.")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsante per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)
    # Pulsanti per la gestione dell'inserimento del prezzo di un nuovo strumento
    pulsante_incrementa_prezzo = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", on_click=incrementa_prezzo)
    pulsante_decrementa_prezzo = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", on_click=decrementa_prezzo)

    # --- LAYOUT ---
    page.add(
        ft.Row(
            controls=[toggle_cambia_tema],
            alignment=ft.MainAxisAlignment.START        #allineo a sinistra il pulsante per cambiare tema
        ),

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),                                          #aggiungo una riga divisoria
        ft.Text("Aggiungi nuovo strumento", size=20),          #aggiungo il titolo della sezione
        ft.Row(spacing=30,        #creo una riga con tutti i campi per aggiungere un nuovo strumento e li equidistanzio
               controls=[input_tipo, input_marca, input_anno,
               ft.Row([pulsante_decrementa_prezzo, input_prezzo, pulsante_incrementa_prezzo])], #creo una riga interna
               alignment=ft.MainAxisAlignment.CENTER),      #allineo la riga con i comandi per l'inserimento del prezzo
        pulsante_aggiungi_strumento,                        #aggiungo il pulsante per aggiungere il nuovo strumento

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
