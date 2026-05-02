# Xerox Virtual

![Python](https://img.shields.io/badge/python-3.11-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)

Ferramenta de captura de tela que detecta automaticamente quando as páginas estão totalmente renderizadas antes de capturar, a fim de evitar imagens borradas/incompletas. Inclui seleção de área via interface gráfica (tkinter), navegação gráfica entre páginas e exportação em PDF.

## Aviso de uso

Este projeto é destinado para uso educacional e automação de captura em conteúdos próprios ou públicos.

O uso para capturar ou redistribuir conteúdo protegido por direitos autorais pode violar termos de serviço ou leis locais. O usuário é responsável pelo uso da ferramenta.

## Funcionalidades
- Seleção de área da tela estilo ferramenta de recorte
- Automação de navegação (cliques automáticos)
- Detecção inteligente de carregamento (sem delay fixo)
- Interrupção a qualquer momento com tecla ESC
- Exportação automática para PDF
- Captura apenas quando a imagem está estável (evita blur)
- Interface gráfica simples (sem necessidade de terminal)

## Motivação

Este projeto foi criado para automatizar a captura de conteúdos paginados que não permitem exportação direta, simulando o comportamento de um scanner digital.

---------------------------------------
## Requisitos
- Python 3.10+
- Windows (testado)
- Tela com resolução estável durante execução

## Instalação
1. Clone o repositório
  ```
  git clone https://github.com/joaodyba/xerox-virtual.git
  cd xerox-virtual
  ```
2. Instale as dependências
```
pip install pyautogui pillow mss numpy keyboard img2pdf
```

## Estrutura do projeto

```
xerox-virtual/
│── index.py
│── README.md
│── LICENSE
```

## Como deve ser utilizado
1. Execute o script:
```
python index.py
```
2. A interface irá abrir
3. Siga essas instruções:
   - Clique em **"Selecionar área"**
   - Arraste para escolher a região da tela
   - Pressione `ENTER` para confirmar
   - Clique em **"Capturar botão"**
   - Posicione o mouse sobre o botão de próxima página
   - Aguarde alguns segundos
   - Defina o número de páginas
   - Clique em **"Iniciar"**
4. O programa irá:
   - Capturar a primeira imagem
   - Navegar automaticamente entre páginas
   - Esperar o carregamento completo
   - Evitar capturas duplicadas
   - Gerar um PDF final automaticamente

## Controles
| Tecla        | Ação |
|--------------|------|
| `ESC`        | Interrompe o processo imediatamente |
| `ENTER`      | Confirma a seleção da área |

## Saída
O arquivo final será gerado automaticamente como:
```
resultado.pdf
```
----------------------------------------------
## Como funciona

O programa:

1. Captura uma área da tela definida pelo usuário  
2. Detecta mudanças entre frames  
3. Aguarda até que a imagem esteja estável  
4. Realiza a captura  
5. Repete o processo automaticamente  
6. Gera um PDF final com todas as páginas  

### Características

- Cada captura corresponde a uma página do PDF  
- Imagens com a qualidade baseada no tamanho da região da tela
- Ordem sequencial automática  
- Geração rápida utilizando `img2pdf`  

### Observações

- O arquivo é salvo no mesmo diretório do script  
- Arquivos temporários são removidos automaticamente após a geração
  
---------------------------
## Licença
Este projeto está sob a licença MIT.
