from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import random
import os
from selenium.webdriver.chrome.options import Options

# ==========================================
# CONFIGURATION
# ==========================================

# Les numéros sont chargés depuis le fichier numeros.txt (un numéro par ligne)
# Ce fichier est dans .gitignore pour protéger les données personnelles
def charger_numeros(fichier="numeros.txt"):
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), fichier)
    if not os.path.exists(chemin):
        print(f"❌ Fichier '{fichier}' introuvable. Créez-le avec un numéro par ligne.")
        exit(1)
    with open(chemin, "r", encoding="utf-8") as f:
        return [ligne.strip() for ligne in f if ligne.strip()]

NUMEROS = charger_numeros()

MESSAGE = """Votre message ici...
Modifiez ce texte dans le fichier whatsapp_sender.py"""

# ==========================================
# SCRIPT
# ==========================================
import os

# Chemin absolu vers le dossier du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_SUIVI = os.path.join(SCRIPT_DIR, "deja_envoyes.txt")

def charger_deja_envoyes():
    if not os.path.exists(FICHIER_SUIVI):
        return set()
    with open(FICHIER_SUIVI, "r", encoding="utf-8") as f:
        return set([ligne.strip() for ligne in f.readlines() if ligne.strip()])

def sauvegarder_succes(numero):
    with open(FICHIER_SUIVI, "a", encoding="utf-8") as f:
        f.write(f"{numero}\n")

def envoyer_messages_prives(numeros, message):
    print("Démarrage de Brave...")
    options = Options()
    options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    
    # Utiliser votre VRAI profil Brave personnel au lieu d'un nouveau
    user_data_dir = r"C:\Users\VOTRE_NOM\AppData\Local\BraveSoftware\Brave-Browser\User Data"
    options.add_argument(f"user-data-dir={user_data_dir}")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    
    print("En attente du chargement de WhatsApp Web...")
    print("\n👉 ACTION REQUISE : Regardez la fenêtre Brave.")
    print("👉 Une fois que WhatsApp Web est complètement chargé et que vous voyez vos conversations,")
    input("👉 APPUYEZ SUR LA TOUCHE 'ENTRÉE' de votre clavier ici pour lancer les envois... ")
    
    print("✅ C'est parti !")

    message_encode = urllib.parse.quote(message)
    deja_envoyes = charger_deja_envoyes()
    total = len(numeros)
    
    time.sleep(5)
    echecs_consecutifs = 0
    
    for i, numero in enumerate(numeros, 1):
        if numero in deja_envoyes:
            print(f"[{i}/{total}] ⏭️ Ignoré : le message a déjà été envoyé au {numero} précédemment.")
            continue
            
        # Rafraîchir la page tous les 10 envois pour éviter que WhatsApp Web ne plante ou ne sature la mémoire
        if i % 10 == 0:
            print("🔄 Rafraîchissement de la page pour éviter les bugs de mémoire...")
            driver.refresh()
            time.sleep(10)
            
        print(f"[{i}/{total}] ⏳ Chargement de la conversation pour le {numero}...")
        try:
            url = f"https://web.whatsapp.com/send?phone={numero}&text={message_encode}"
            driver.get(url)
            
            bouton_envoi = None
            temps_debut = time.time()
            
            # 45 secondes sont amplement suffisantes si la page n'est pas bloquée
            while time.time() - temps_debut < 45:
                try:
                    xpaths = [
                        '//span[@data-icon="send"]/..',
                        '//span[@data-icon="send"]',
                        '//button[@aria-label="Envoyer"]',
                        '//button[@aria-label="Send"]'
                    ]
                    for xp in xpaths:
                        elements = driver.find_elements(By.XPATH, xp)
                        if len(elements) > 0 and elements[0].is_displayed() and elements[0].is_enabled():
                            bouton_envoi = elements[0]
                            break
                    if bouton_envoi:
                        break
                        
                    # Détection stricte du message d'erreur de WhatsApp pour éviter les faux positifs
                    erreur_texte = driver.find_elements(By.XPATH, '//*[contains(text(), "via l\'URL n\'est pas valide") or contains(text(), "via url is invalid")]')
                    if len(erreur_texte) > 0:
                        print(f"⚠️ WhatsApp a indiqué que {numero} est invalide.")
                        break
                        
                except Exception:
                    pass
                time.sleep(1)
            
            if bouton_envoi:
                bouton_envoi.click()
                print(f"✅ Message envoyé au {numero}.")
                sauvegarder_succes(numero) # On l'enregistre pour ne plus jamais lui envoyer
                echecs_consecutifs = 0
                
                delai = random.randint(28, 35)
                print(f"⏳ Pause de {delai}s avant le prochain envoi...")
                time.sleep(delai)
            else:
                # Si ça échoue encore, on essaie d'appuyer sur Entrée dans la zone de texte
                try:
                    boite_texte = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    boite_texte.send_keys(Keys.ENTER)
                    print(f"✅ Message envoyé au {numero} (via la touche Entrée).")
                    sauvegarder_succes(numero)
                    echecs_consecutifs = 0
                    time.sleep(random.randint(28, 35))
                except:
                    print(f"❌ Échec pour {numero} après 45s d'attente.")
                    echecs_consecutifs += 1
                    
                    # Si 3 échecs de suite, le navigateur a probablement planté. On rafraîchit.
                    if echecs_consecutifs >= 3:
                        print("⚠️ 3 échecs consécutifs détectés. Rafraîchissement forcé de WhatsApp pour débloquer...")
                        driver.refresh()
                        time.sleep(10)
                        echecs_consecutifs = 0
            
        except Exception as e:
            print(f"❌ Erreur système avec le numéro {numero}.")
            
    print("🎉 Traitement terminé.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    envoyer_messages_prives(NUMEROS, MESSAGE)


