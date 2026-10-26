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
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno_acquisto = ft.TextField(label="Anno acquisto")

    # Creo il contatore con i suoi pulsanti -, + e il bottone "Aggoiungi strumento"
    casella_contatore = ft.TextField(value = "0",
                                     disabled = True,
                                     width = 80,
                                     text_align = ft.TextAlign.CENTER,)

    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24)


    btn_piu = ft.IconButton(icon=ft.Icons.ADD,
                            icon_color="green",
                            icon_size=24)

    btn_aggiungi = ft.Button("Aggiungi strumento")



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
    def dimiuisci_prezzo(e):
        v = int(casella_contatore.value)
        if v > 0:                        #visto che gli strumenti non possono assumere valore neg
            v = v - 1
        casella_contatore.value = str(v)
        casella_contatore.update()

    def aumenta_prezzo(e):
        v = int(casella_contatore.value)
        v = v+1
        casella_contatore.value = str(v)
        casella_contatore.update()

    def aggiungi_strumento(e):
        # recupero dei valori inseriti nella caselle
        tipo = input_tipo.value
        marca = input_marca.value
        anno_acquisto = input_anno_acquisto.value

        #controllo campi di testo obbligatori
        if not tipo or not tipo.strip():
            alert.show_alert("Inserire il tipo di strumento!")
            return
        if not marca or not marca.strip():
            alert.show_alert("Inserire la marca dello strumento!")
            return
        #controllo dell'anno
        try:
            anno_acquisto = int(input_anno_acquisto.value)
            if anno_acquisto <= 0:
                alert.show_alert("L'anno d'acquisto deve essere positivo!")
                return
        except ValueError:
            alert.show_alert("L'anno d'acquisto deve essere un numero valido!")
            return
        #controllo valore casella contatore
        try:
            valore = float(casella_contatore.value)
            if valore <= 0:
                alert.show_alert("Il prezzo dello strumento deve essere maggiore di zero!")
                return
        except ValueError:
            alert.show_alert("Il prezzo inserito non è valido!")
            return

        #aggiunta dello strumento al deposito
        deposito.aggiungi_strumento(tipo.strip(), marca.strip(), anno_acquisto, valore)

        #svoto le caselle di testo
        input_tipo.value = ""
        input_marca.value = ""
        input_anno_acquisto.value = ""
        casella_contatore.value = "0"

        aggiorna_lista_strumenti()
        page.update()




    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_meno.on_click = dimiuisci_prezzo
    btn_piu.on_click = aumenta_prezzo
    btn_aggiungi.on_click = aggiungi_strumento


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

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
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(controls=[input_tipo, input_marca, input_anno_acquisto, btn_meno, casella_contatore,btn_piu],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[btn_aggiungi],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),      #riga orizzontale di separazione
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
