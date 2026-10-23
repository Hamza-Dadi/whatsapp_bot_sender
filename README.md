# 📱 WhatsApp Bot Sender

Un script Python automatisé pour envoyer des messages privés en masse via **WhatsApp Web**, en utilisant **Selenium** avec le navigateur **Brave**.

---

## ✨ Fonctionnalités

- ✅ Envoi automatique de messages à une liste de numéros
- ✅ Utilise votre session WhatsApp déjà connectée (pas besoin de scanner le QR code à chaque fois)
- ✅ Sauvegarde des numéros déjà traités pour reprendre sans doublon
- ✅ Rafraîchissement automatique de la page toutes les 10 envois (anti-blocage mémoire)
- ✅ Délai aléatoire entre chaque envoi pour éviter la détection anti-spam
- ✅ Détection automatique des numéros invalides (non enregistrés sur WhatsApp)
- ✅ Déblocage intelligent en cas d'échecs consécutifs

---

## 🛠️ Prérequis

- Python 3.x
- Navigateur [Brave](https://brave.com/)
- [ChromeDriver](https://chromedriver.chromium.org/) compatible avec votre version de Brave
- La bibliothèque Selenium :

```bash
pip install selenium
```

---

## ⚙️ Configuration

Ouvrez `whatsapp_sender.py` et modifiez les variables suivantes :

```python
# Liste des numéros (avec l'indicatif pays, sans le +)
NUMEROS = [
    "212XXXXXXXXX",
    "212XXXXXXXXX",
    ...
]

# Le message à envoyer
MESSAGE = """Votre message ici..."""
```

Assurez-vous que le chemin vers Brave et votre profil utilisateur sont corrects :

```python
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
user_data_dir = r"C:\Users\VOTRE_NOM\AppData\Local\BraveSoftware\Brave-Browser\User Data"
```

---

## 🚀 Utilisation

1. **Fermez complètement Brave** avant de lancer le script
2. Lancez le script :

```bash
py whatsapp_sender.py
```

3. Une fenêtre Brave s'ouvre sur WhatsApp Web
4. Attendez que WhatsApp Web soit **complètement chargé** (vous voyez vos conversations)
5. Appuyez sur **Entrée** dans le terminal pour lancer les envois

---

## 📂 Structure du projet

```
whatsapp_bot_sender/
│
├── whatsapp_sender.py   # Script principal
├── deja_envoyes.txt     # Numéros déjà traités (généré automatiquement)
└── README.md            # Ce fichier
```

---

## ⚠️ Avertissements

- **Respect des CGU** : L'envoi automatisé de messages peut enfreindre les [Conditions d'utilisation de WhatsApp](https://www.whatsapp.com/legal/terms-of-service). Utilisez ce script de façon responsable.
- **Anti-spam** : WhatsApp peut restreindre temporairement votre compte si trop de messages sont envoyés rapidement. Le délai de 30 secondes entre chaque envoi est recommandé.
- **Données personnelles** : Ne partagez pas publiquement votre fichier `deja_envoyes.txt` car il contient des numéros de téléphone.

---

## 🧰 Technologies utilisées

- [Python 3](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [Brave Browser](https://brave.com/)
- WhatsApp Web API URL (`web.whatsapp.com/send?phone=...`)

---

## 📄 Licence

Ce projet est à usage personnel et éducatif uniquement.
