# DriverTool

DriverTool é um pequeno utilitário para **reparo do sistema operacional Windows** e **backup de drivers e informações do sistema**.

O objetivo do projeto é reunir e automatizar algumas **ferramentas nativas do Windows** para facilitar a manutenção do sistema, diagnóstico e recuperação.

## ✨ Funcionalidades

* 🔧 Reparar arquivos do sistema usando ferramentas do Windows
* 💾 Fazer **backup de drivers instalados**
* 📊 Coletar **informações do sistema**
* ⚙️ Executar comandos úteis de manutenção do Windows
* 🧰 Centralizar ferramentas de diagnóstico em um único lugar

## 🛠️ Ferramentas Utilizadas

O DriverTool utiliza recursos nativos do Windows, como:

* `sfc /scannow`
* `DISM`
* `driverquery`
* `pnputil`
* `systeminfo`

Essas ferramentas ajudam a identificar problemas no sistema e realizar reparos automaticamente.

## 📦 Estrutura do Projeto

```
DriverTool
│
├── scripts/
│   ├── repair.bat
│   ├── backup_drivers.bat
│   └── system_info.bat
│
├── backup/
├── logs/
└── README.md
```

## 🚀 Como Usar

1. Baixe ou clone o repositório:

```
git clone https://github.com/seuusuario/drivertool.git
```

2. Execute o script principal como **Administrador**.

3. Escolha a opção desejada no menu:

* Reparar sistema
* Fazer backup de drivers
* Coletar informações do sistema

## ⚠️ Requisitos

* Windows 10 ou superior
* Permissão de Administrador
* PowerShell ou Prompt de Comando

## 📌 Objetivo do Projeto

Este projeto foi criado para **estudo, automação de manutenção de Windows e recuperação de sistemas**, reunindo comandos úteis em uma ferramenta simples.

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e contribuir.

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório.

![Uploading DRIVERTOOL.jpg…]()

