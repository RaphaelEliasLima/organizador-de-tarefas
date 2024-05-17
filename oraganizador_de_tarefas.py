import PySimpleGUI as sg
import json
import os
import time

# Modo de depuração
DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(msg)

# Nome dos arquivos onde as tarefas serão salvas
FILENAME = 'tarefas.json'
COMPLETED_FILENAME = 'tarefas_concluidas.json'

# Função para carregar tarefas do arquivo
def carregar_tarefas():
    try:
        if os.path.exists(FILENAME):
            with open(FILENAME, 'r') as file:
                debug_print("Tarefas carregadas do arquivo")
                return json.load(file)
    except Exception as e:
        debug_print(f"Erro ao carregar tarefas: {e}")
    return []

# Função para salvar tarefas no arquivo
def salvar_tarefas(tarefas):
    try:
        with open(FILENAME, 'w') as file:
            json.dump(tarefas, file)
            debug_print("Tarefas salvas no arquivo")
    except Exception as e:
        debug_print(f"Erro ao salvar tarefas: {e}")

# Função para carregar tarefas concluídas do arquivo
def carregar_tarefas_concluidas():
    try:
        if os.path.exists(COMPLETED_FILENAME):
            with open(COMPLETED_FILENAME, 'r') as file:
                debug_print("Tarefas concluídas carregadas do arquivo")
                return json.load(file)
    except Exception as e:
        debug_print(f"Erro ao carregar tarefas concluídas: {e}")
    return []

# Função para salvar tarefas concluídas no arquivo
def salvar_tarefas_concluidas(tarefas):
    try:
        with open(COMPLETED_FILENAME, 'w') as file:
            json.dump(tarefas, file)
            debug_print("Tarefas concluídas salvas no arquivo")
    except Exception as e:
        debug_print(f"Erro ao salvar tarefas concluídas: {e}")

# Função para obter a hora atual
def atualizar_relogio():
    return time.strftime('%H:%M:%S')

# Função para criar a janela inicial
def criar_janela_inicial(tarefas):
    sg.theme("DarkBlue4")
    
    try:
        layout = [
            [
                sg.Frame(
                    'Tarefas',
                    layout=[
                        [
                            sg.Checkbox('', key=f"tarefa_{i}", default=tarefa.get('checked', False)), 
                            sg.Input(tarefa.get('text', ''), key=f"input_{i}")
                        ] for i, tarefa in enumerate(tarefas) if isinstance(tarefa, dict)
                    ],
                    key='container'
                )
            ],
            [sg.Button('Nova tarefa'), sg.Button('Resetar')],
            [sg.Button('Salvar'), sg.Button('Tarefas Concluídas')],
            [sg.Text('', key='relogio', font=('Helvetica', 16), size=(20, 1), justification='right')]
        ]
        
        return sg.Window('Organizador de Tarefas', layout=layout, finalize=True)
    except Exception as e:
        print(f"Erro ao criar a janela: {e}")

# Função para criar a janela de tarefas concluídas
def criar_janela_concluidas(tarefas_concluidas):
    sg.theme("DarkBlue4")
    layout = [
        [sg.Text('Tarefas Concluídas', font=('Helvetica', 16))],
        [sg.Listbox(values=[f"{tarefa['text']} - {tarefa['time']}" for tarefa in tarefas_concluidas], size=(50, 10), key='lista_concluidas')],
        [sg.Button('Voltar')]
    ]
    return sg.Window('Tarefas Concluídas', layout=layout, finalize=True)

def main():
    # Carregar tarefas e tarefas concluídas do arquivo
    tarefas = carregar_tarefas()
    tarefas_concluidas = carregar_tarefas_concluidas()

    # Criar a janela inicial
    janela = criar_janela_inicial(tarefas)

    # Loop principal da aplicação
    while True:
        event, values = janela.read(timeout=1000)

        if event == sg.WIN_CLOSED:
            debug_print("Janela fechada pelo usuário")
            break

        # Atualizar o relógio a cada segundo
        current_time = atualizar_relogio()
        janela['relogio'].update(current_time)
        debug_print(f"Relógio atualizado: {current_time}")

        # Adicionar uma nova tarefa
        if event == 'Nova tarefa':
            i = len(tarefas)
            janela.extend_layout(janela['container'], [[sg.Checkbox('', key=f"tarefa_{i}"), sg.Input('', key=f"input_{i}")]])
            tarefas.append({'checked': False, 'text': ''})
            debug_print("Nova tarefa adicionada")

        # Resetar as tarefas
        if event == 'Resetar':
            janela.close()
            tarefas = []
            janela = criar_janela_inicial(tarefas)
            debug_print("Tarefas resetadas")

        # Salvar tarefas
        if event == 'Salvar':
            for i, tarefa in enumerate(tarefas):
                tarefa['checked'] = values[f'tarefa_{i}']
                tarefa['text'] = values[f'input_{i}']
            salvar_tarefas(tarefas)
            debug_print("Tarefas salvas")

            # Adicionar tarefas concluídas ao arquivo de tarefas concluídas
            for tarefa in tarefas:
                if tarefa['checked'] and tarefa['text']:
                    tarefas_concluidas.append({'text': tarefa['text'], 'time': current_time})
                    tarefa['checked'] = False
                    tarefa['text'] = ''

            salvar_tarefas_concluidas(tarefas_concluidas)

        # Mostrar tarefas concluídas
        if event == 'Tarefas Concluídas':
            janela.hide()
            janela_concluidas = criar_janela_concluidas(tarefas_concluidas)
            while True:
                event_concluidas, _ = janela_concluidas.read()
                if event_concluidas == sg.WIN_CLOSED or event_concluidas == 'Voltar':
                    janela_concluidas.close()
                    janela.un_hide()
                    break

    # Fechar a janela
    janela.close()
    debug_print("Janela fechada")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        debug_print(f"Erro ao executar a aplicação: {e}")
        input("Pressione Enter para sair...")
