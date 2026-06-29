from pysap import SapConfig, start_session
from pysap.objects import GuiRadioButton

session = start_session(SapConfig.from_env(dotenv_path=".env"))

# 1. Abrir una transacción (cámbiala por una tuya de solo lectura, p.ej. SE16, VA03)


# 3. ¿Hay popup? Manéjalo
if session.has_popup(1):
    print("Popup detectado, confirmando...")
    # session.send_vkey(40, 1)
    session.find_as("wnd[1]/usr/radMULTI_LOGON_OPT2", kind=GuiRadioButton).select()
    session.confirm_popup(1)

if session.has_popup(1):
    print("Popup detectado, cancelando...")
    session.confirm_popup(1)

session.start_transaction("SE16N")  # Cambia por la transacción que quieras abrir
estado = session.status()
print("Estado:", estado.type, "-", estado.text)
