# 🛡️ VT TUI Scanner
[![CI](https://github.com/valorisa/VT-TUI-Scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/valorisa/VT-TUI-Scanner/actions/workflows/ci.yml)
[![Security](https://github.com/valorisa/VT-TUI-Scanner/actions/workflows/ci.yml/badge.svg?job=security-scan)](...)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/github/stars/valorisa/VT-TUI-Scanner)](https://github.com/valorisa/VT-TUI-Scanner/stargazers)
[![Forks](https://img.shields.io/github/forks/valorisa/VT-TUI-Scanner)](https://github.com/valorisa/VT-TUI-Scanner/network/members)

## 📋 Description Détaillée

**VT TUI Scanner** est une application terminal moderne et interactive (TUI - Terminal User Interface) conçue pour faciliter l'analyse de fichiers, de dossiers et d'URLs via l'API VirusTotal. Développé en Python avec le framework Textual, cet outil offre une expérience utilisateur riche tout en restant léger et cross-platform.

### 🎯 Pourquoi VT TUI Scanner ?

Dans un contexte de cybersécurité où la rapidité et l'efficacité sont cruciales, VT TUI Scanner répond aux besoins des professionnels de la sécurité, des administrateurs système et des développeurs qui souhaitent :

- **Automatiser** l'analyse de multiples fichiers sans interface graphique lourde
- **Surveiller** des dossiers sensibles en temps réel
- **Exporter** des rapports d'analyse pour audit et conformité
- **Respecter** les limites de l'API VirusTotal (rate-limiting intelligent)
- **Intégrer** facilement dans des pipelines CI/CD et des conteneurs Docker

### 🔐 Cas d'Usage Principaux

1. **Analyse de Fichiers Suspicious** - Scanner rapidement des fichiers téléchargés ou reçus
2. **Surveillance de Dossiers** - Monitorer des dossiers de téléchargement ou de partage
3. **Vérification d'URLs** - Valider la sécurité de liens avant clic
4. **Reporting de Sécurité** - Générer des rapports pour audits internes
5. **Intégration DevSecOps** - Inclure dans des pipelines de sécurité automatisés

---

## ✨ Fonctionnalités Complètes

### 🖥️ Interface TUI Moderne
- Navigation clavier et souris intuitive
- Thèmes sombre/clair configurables
- Barres de progression en temps réel
- Tableaux de résultats interactifs
- Logs visibles directement dans l'interface

### 📁 Capacités de Scan
| Type | Description | Rate-Limit Aware |
|------|-------------|------------------|
| Fichier Unique | Analyse d'un fichier spécifique | ✅ |
| Dossier Complet | Scan récursif avec filtrage par extension | ✅ |
| Surveillance | Watch mode pour nouveaux/modifiés fichiers | ✅ |
| URL | Vérification de liens web | ✅ |
| Batch | Multiple URLs en une session | ✅ |

### 📊 Export et Reporting
- **JSON** - Format structuré pour intégration API
- **CSV** - Compatible Excel/Sheets pour reporting
- **Historique Local** - Tracking des scans précédents
- **Timestamps** - Horodatage précis de chaque analyse

### 🔒 Sécurité et Confidentialité
- API keys via variables d'environnement (jamais en dur)
- Fichier `.env` ignoré par Git (.gitignore configuré)
- Logs sécurisés sans données sensibles
- Respect strict des quotas API VirusTotal

### 🐳 Déploiement Flexible
- **Native** - Installation Python standard
- **Docker** - Conteneurisation prête à l'emploi
- **Headless** - Mode sans TUI pour automation
- **CI/CD** - Workflows GitHub Actions inclus

---

## 📋 Prérequis Techniques

### Système d'Exploitation
- ✅ Windows 10/11 (Testé sur Windows 11 Enterprise)
- ✅ macOS 12+ (Monterey, Ventura, Sonoma)
- ✅ Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)

### Python
- Version minimale : **Python 3.9**
- Version recommandée : **Python 3.11+**
- Gestionnaire de paquets : **pip** inclus

### API VirusTotal
- Compte gratuit : [virustotal.com](https://www.virustotal.com)
- API Key gratuite : 4 req/min, 500 req/jour
- API Key premium : Limites étendues disponibles

### Outils Optionnels
- **Git** - Pour cloner le repository
- **Docker** - Pour usage containerisé
- **GitHub CLI (gh)** - Pour création rapide de repo

---

## 🚀 Installation Complète

### Méthode 1 : Installation depuis Source (Recommandée)

```powershell
# 1. Cloner le repository
git clone https://github.com/valorisa/vt-tui-scanner.git
cd vt-tui-scanner

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement (PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer l'API Key
copy .env.example .env
# Éditer .env et ajouter votre VT_API_KEY
```

### Méthode 2 : Installation Docker

```powershell
# Build de l'image
docker build -t vt-tui-scanner .

# Run avec variable d'environnement
docker run -it -e VT_API_KEY=votre_cle vt-tui-scanner

# Ou avec docker-compose
docker-compose up vt-scanner
```

### Méthode 3 : Installation PyPI (À venir)

```powershell
pip install vt-tui-scanner
```

---

## ⚙️ Configuration Détaillée

### Configuration de l'API Key

**Option A : Fichier .env (Recommandé)**
```bash
# Copier le fichier exemple
copy .env.example .env

# Éditer avec votre éditeur préféré
notepad .env

# Ajouter votre clé
VT_API_KEY=votre_cle_api_virustotal_ici
```

**Option B : Variable d'Environnement Système**
```powershell
# PowerShell (session actuelle)
$env:VT_API_KEY = "votre_cle_api"

# PowerShell (permanent - nécessite admin)
[Environment]::SetEnvironmentVariable("VT_API_KEY", "votre_cle", "User")

# CMD (permanent)
setx VT_API_KEY "votre_cle"
```

**Option C : Variable d'Environnement Docker**
```yaml
# docker-compose.yml
environment:
  - VT_API_KEY=${VT_API_KEY}
```

### Fichier de Configuration config.yaml

```yaml
# Configuration complète VT TUI Scanner

# Intervalle de surveillance de dossier (en secondes)
scan_interval: 3600

# Export automatique des résultats
auto_export: true

# Format d'export (json, csv, both)
export_format: json

# Niveau de log (DEBUG, INFO, WARNING, ERROR)
log_level: INFO

# Fichier d'historique des scans
history_file: scan_history.json

# Interface
dark_mode: true

# Chemins
exports_directory: ./exports
logs_directory: ./logs
```

---

## 💻 Guide d'Utilisation Complet

### Lancement de l'Interface TUI

```powershell
# Mode interactif avec TUI
python -m src.main

# Ou après installation
vt-tui-scanner
```

**Navigation TUI :**
| Touche | Action |
|--------|--------|
| `q` | Quitter l'application |
| `d` | Basculer mode sombre/clair |
| `f` | Scanner un fichier |
| `d` | Scanner un dossier |
| `u` | Scanner une URL |
| `r` | Voir les résultats |
| `s` | Paramètres |
| `1-4` | Navigation rapide |

### Mode Headless (Automation)

```powershell
# Scanner un fichier unique
vt-tui-scanner --headless --file C:\Downloads\suspect.exe

# Scanner un dossier complet
vt-tui-scanner --headless --dir C:\Downloads

# Scanner une URL
vt-tui-scanner --headless --url https://example.com/suspicious-link

# Avec export des résultats
vt-tui-scanner --headless --dir C:\Downloads --export json

# Mode verbose pour debugging
vt-tui-scanner --headless --file test.exe --verbose
```

### Options de Ligne de Commande

```
usage: vt-tui-scanner [-h] [--headless] [--file FILE] [--url URL] 
                      [--dir DIR] [--config CONFIG] [--export {json,csv,both}] 
                      [--verbose] [--version]

Options:
  --headless          Exécuter sans interface TUI (automation/CI)
  --file FILE         Chemin du fichier à scanner
  --url URL           URL à analyser
  --dir DIR           Dossier à scanner (récursif)
  --config CONFIG     Fichier de configuration (défaut: config.yaml)
  --export FORMAT     Format d'export (json, csv, both)
  --verbose, -v       Activer les logs détaillés
  --version           Afficher la version
```

---

## 📊 Exemples de Sortie

### Résultat de Scan (Console)
```
[2024-01-15 10:30:45] [INFO] VT TUI Scanner starting...
[2024-01-15 10:30:46] [INFO] VTClient initialized
[2024-01-15 10:30:47] [INFO] Uploading file for scan: C:\Downloads\file.exe
[2024-01-15 10:31:15] [INFO] Scan complete: 0/72 detections
[2024-01-15 10:31:15] [INFO] Exported 1 results to exports\scan_results_20240115_103115.json
```

### Export JSON (Extrait)
```json
{
  "export_date": "2024-01-15T10:31:15.123456",
  "total_scans": 1,
  "results": [
    {
      "timestamp": "2024-01-15T10:31:15",
      "scan_type": "file",
      "target": "C:\\Downloads\\file.exe",
      "hash": "abc123def456...",
      "positives": 0,
      "total": 72,
      "status": "completed",
      "permalink": "https://www.virustotal.com/file/abc123...",
      "risk_level": "clean"
    }
  ]
}
```

---

## 🧪 Tests et Validation

### Exécuter la Suite de Tests

```powershell
# Tous les tests
pytest tests/

# Avec rapport de couverture
pytest tests/ --cov=src --cov-report=html

# Test spécifique
pytest tests/test_vt_client.py -v

# Ouvrir le rapport de couverture
start htmlcov\index.html
```

### Validation de Qualité

```powershell
# Linting
flake8 src/ tests/ --max-line-length=100

# Formatage
black src/ tests/

# Type checking
mypy src/
```

---

## 🔧 Dépannage (Troubleshooting)

### Problème : API Key non trouvée
```powershell
# Vérifier la variable
echo $env:VT_API_KEY

# Si vide, reconfigurer
copy .env.example .env
# Éditer .env avec votre clé
```

### Problème : Rate Limit Exceeded
```
Solution : L'API gratuite est limitée à 4 req/min et 500 req/jour.
- Attendre la fin de la fenêtre de rate-limit
- Utiliser le file tracking pour éviter les re-scans
- Considérer une API key premium pour usage intensif
```

### Problème : Module non trouvé
```powershell
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier l'environnement virtuel
.\venv\Scripts\Activate.ps1
```

### Problème : TUI ne s'affiche pas correctement
```powershell
# Mettre à jour Textual
pip install --upgrade textual

# Vérifier la taille du terminal
# La TUI nécessite minimum 80x24 caractères
```

---

## 📁 Structure du Projet

```
vt-tui-scanner/
├── src/                      # Code source principal
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Entry point
│   ├── tui/                  # Interface utilisateur
│   │   ├── app.py            # Application principale
│   │   ├── screens.py        # Écrans TUI
│   │   └── widgets.py        # Widgets personnalisés
│   ├── scanner/              # Logique de scan
│   │   ├── vt_client.py      # Client API VirusTotal
│   │   ├── file_scanner.py   # Scan de fichiers
│   │   └── url_scanner.py    # Scan d'URLs
│   ├── utils/                # Utilitaires
│   │   ├── config.py         # Configuration
│   │   ├── logger.py         # Logging
│   │   └── export.py         # Export résultats
│   └── models/               # Modèles de données
│       └── scan_result.py    # Modèle de résultat
├── tests/                    # Tests unitaires
├── .github/workflows/        # CI/CD
├── exports/                  # Résultats exportés
├── .env.example              # Template configuration
├── .gitignore                # Git exclusions
├── Dockerfile                # Containerisation
├── docker-compose.yml        # Orchestration
├── requirements.txt          # Dépendances Python
├── pyproject.toml           # Configuration projet
├── LICENSE                   # Licence MIT
├── README.md                 # Ce fichier
├── CONTRIBUTING.md           # Guide contribution
└── CHANGELOG.md              # Historique versions
```

---

## 🔒 Notes de Sécurité Importantes

### ⚠️ Avertissements

1. **API Key** - Ne jamais commiter `.env` dans Git
2. **Fichiers Scannés** - Les fichiers uploadés sont stockés par VirusTotal
3. **Données Sensibles** - Ne pas scanner de fichiers contenant des secrets
4. **Rate Limiting** - Respecter les quotas pour éviter le bannissement

### ✅ Bonnes Pratiques

- Utiliser des API keys dédiées par projet
- Rotater les clés régulièrement
- Monitorer l'usage API dans le dashboard VirusTotal
- Chiffrer les exports contenant des résultats sensibles

---

## 🤝 Contribuer au Projet

### Comment Contribuer ?

1. **Fork** le repository
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commit** les changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Pull Request** vers `main`

### Standards de Code

- **PEP 8** - Style Python officiel
- **Type Hints** - Annotations de type obligatoires
- **Docstrings** - Google style pour documentation
- **Tests** - Couverture minimale 70% sur fonctions critiques

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour le guide complet.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour les détails.

### Vous Pouvez :
- ✅ Utiliser commercialement
- ✅ Modifier le code
- ✅ Distribuer des copies
- ✅ Utiliser dans des projets privés

### Vous Devez :
- ℹ️ Inclure la notice de copyright
- ℹ️ Inclure la licence dans les distributions

---

## 🙏 Remerciements

- **[VirusTotal](https://www.virustotal.com)** - Pour l'API gratuite et les services
- **[Textual](https://textual.textualize.io)** - Framework TUI exceptionnel
- **[Python Community](https://www.python.org)** - Pour l'écosystème riche
- **Tous les contributeurs** - Pour leurs améliorations

---

## 📞 Support et Contact

| Canal | Lien |
|-------|------|
| 🐛 Issues | [GitHub Issues](https://github.com/valorisa/vt-tui-scanner/issues) |
| 📖 Wiki | [GitHub Wiki](https://github.com/valorisa/vt-tui-scanner/wiki) |
| 📧 Email | community@example.com |
| 💬 Discussions | [GitHub Discussions](https://github.com/valorisa/vt-tui-scanner/discussions) |

---

## 📈 Roadmap

### Version 1.0 (Actuelle)
- [x] TUI de base
- [x] Scan fichiers/URLs
- [x] Export JSON/CSV
- [x] Docker support
- [x] CI/CD pipeline

### Version 1.1 (Planifiée)
- [ ] Notifications desktop
- [ ] Scan planifié (cron-like)
- [ ] Thèmes personnalisables
- [ ] Support multi-API keys

### Version 2.0 (Future)
- [ ] Interface GUI optionnelle
- [ ] Multi-threading pour gros dossiers
- [ ] Intégration autres plateformes TI
- [ ] Système de plugins

---

<div align="center">

**⭐ Si vous aimez ce projet, n'oubliez pas de mettre une étoile sur GitHub ! ⭐**

[Faire un Star](https://github.com/valorisa/vt-tui-scanner) | [Fork](https://github.com/valorisa/vt-tui-scanner/fork) | [Issues](https://github.com/valorisa/vt-tui-scanner/issues)

</div>

