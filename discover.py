# -*- coding: utf-8 -*-
import os
import re
import sys
from datetime import datetime

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# --- Configurações ---
# O caminho do projeto será solicitado via argumento de linha de comando.
JAVA_FILE_EXT = '.java'
JSF_FILE_EXT = ['.xhtml', '.jsf']
OUTPUT_FOLDER = 'output'

# Código de erro amigável quando a pasta do projeto não é fornecida
ERROR_CODE_MISSING_PROJECT = 2

# --- Padrões Comuns de Anotações/Arquivos ---
ENTITY_PATTERNS = [
    r'@Entity\b',
    r'@Table\b',
]

BUSINESS_PATTERNS = [
    r'@Named\b',
    r'@Controller\b',
    r'@Service\b',
    r'@RestController\b',
    r'@ManagedBean\b',
    r'extends.*Controller\b',
]

# --- Variáveis de Contagem ---
entity_classes = {}
jsf_pages = []
business_components = {}
db_info_placeholder = "Nenhuma informação de DB capturada de forma automática neste script."
analysis_log = ""
PROJECT_PATH = ""  # Será definido na execução

def analyze_java_file(filepath):
    """Analisa um arquivo .java para Entidades e Componentes de Negócio."""
    global analysis_log
    content = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        analysis_log += f"ERRO ao ler {filepath}: {e}\n"
        return

    found_entity_patterns = [p for p in ENTITY_PATTERNS if re.search(p, content)]
    if found_entity_patterns:
        entity_classes[filepath] = found_entity_patterns

    if not found_entity_patterns:
        found_business_patterns = [p for p in BUSINESS_PATTERNS if re.search(p, content)]
        if found_business_patterns:
            business_components[filepath] = found_business_patterns

def analyze_jsf_file(filepath):
    """Adiciona a página JSF à lista de encontrados."""
    jsf_pages.append(filepath)

def capture_database_info(project_root):
    """Tenta capturar informações básicas do DB."""
    global db_info_placeholder
    db_info_list = []
    config_files = ['.properties', '.xml', '.yml', '.yaml']

    for root, _, files in os.walk(project_root):
        for file in files:
            if any(file.endswith(ext) for ext in config_files):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        info = []
                        if re.search(r'jdbc[:/]?.*url|jdbc:|spring.datasource.url', content, re.IGNORECASE):
                            info.append("Possível URL JDBC")
                        if re.search(r'hibernate\.dialect', content, re.IGNORECASE):
                            info.append("Dialeto Hibernate/JPA")
                        if re.search(r'spring\.datasource', content, re.IGNORECASE):
                            info.append("Configuração Spring Datasource")
                        if info:
                            db_info_list.append(f"- **{os.path.basename(file)}** ({', '.join(info)}) em `{filepath}`")
                except Exception:
                    pass

    if db_info_list:
        db_info_placeholder = "### Arquivos de Configuração de Banco de Dados Encontrados\n" + "\n".join(db_info_list)
    else:
        db_info_placeholder = "Não foram encontrados arquivos de configuração de DB comuns (.properties, .xml, .yml)."

def run_analysis(project_root):
    """Percorre a pasta do projeto e chama as funções de análise."""
    global analysis_log

    analysis_log += f"Iniciando análise do projeto em: {project_root}\n"
    analysis_log += f"Hora de início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    capture_database_info(project_root)

    for root, _, files in os.walk(project_root):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(JAVA_FILE_EXT):
                analyze_java_file(filepath)
            elif any(file.endswith(ext) for ext in JSF_FILE_EXT):
                analyze_jsf_file(filepath)

    analysis_log += "Análise de Arquivos Concluída.\n"

def create_output_folder(project_path):
    """Cria a pasta de saída dentro do projeto se não existir."""
    output_path = os.path.join(project_path, OUTPUT_FOLDER)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"📁 Pasta '{output_path}' criada com sucesso.")
    return output_path

def generate_excel_report(folder_name, output_path):
    """Gera um relatório em formato Excel (.xlsx)."""
    if not HAS_OPENPYXL:
        print("⚠️  openpyxl não está instalado. Pulando geração de Excel.")
        return None

    try:
        wb = Workbook()
        wb.remove(wb.active)  # Remove a sheet padrão
        
        # Estilos
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=12)
        title_font = Font(bold=True, size=14, color="FFFFFF")
        title_fill = PatternFill(start_color="203864", end_color="203864", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
        left_align = Alignment(horizontal="left", vertical="top", wrap_text=True)

        # Sheet 1: Summary
        ws_summary = wb.create_sheet("Summary", 0)
        ws_summary['A1'] = "RNC Project Discovery - Analysis Report"
        ws_summary['A1'].font = title_font
        ws_summary['A1'].fill = title_fill
        ws_summary.merge_cells('A1:B1')
        
        ws_summary['A3'] = "Project Name:"
        ws_summary['B3'] = folder_name
        ws_summary['A4'] = "Analysis Date:"
        ws_summary['B4'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ws_summary['A5'] = "Project Path:"
        ws_summary['B5'] = PROJECT_PATH
        
        ws_summary['A7'] = "Metric"
        ws_summary['B7'] = "Count"
        for cell in ['A7', 'B7']:
            ws_summary[cell].font = header_font
            ws_summary[cell].fill = header_fill
            ws_summary[cell].alignment = center_align
        
        ws_summary['A8'] = "Entity Classes"
        ws_summary['B8'] = len(entity_classes)
        ws_summary['A9'] = "Business Components"
        ws_summary['B9'] = len(business_components)
        ws_summary['A10'] = "JSF Pages"
        ws_summary['B10'] = len(jsf_pages)
        
        for row in range(8, 11):
            ws_summary[f'A{row}'].alignment = left_align
            ws_summary[f'B{row}'].alignment = center_align
            ws_summary[f'B{row}'].font = Font(bold=True, size=11)

        ws_summary.column_dimensions['A'].width = 25
        ws_summary.column_dimensions['B'].width = 30

        # Sheet 2: Entity Classes
        ws_entities = wb.create_sheet("Entity Classes", 1)
        ws_entities['A1'] = "Entity Classes"
        ws_entities['A1'].font = title_font
        ws_entities['A1'].fill = title_fill
        ws_entities.merge_cells('A1:C1')
        
        ws_entities['A3'] = "File Path"
        ws_entities['B3'] = "Relative Path"
        ws_entities['C3'] = "Patterns Found"
        for cell in ['A3', 'B3', 'C3']:
            ws_entities[cell].font = header_font
            ws_entities[cell].fill = header_fill
            ws_entities[cell].alignment = center_align
            ws_entities[cell].border = border

        row = 4
        for filepath, patterns in entity_classes.items():
            relative_path = os.path.relpath(filepath, PROJECT_PATH)
            patterns_str = ', '.join(patterns)
            ws_entities[f'A{row}'] = filepath
            ws_entities[f'B{row}'] = relative_path
            ws_entities[f'C{row}'] = patterns_str
            for col in ['A', 'B', 'C']:
                ws_entities[f'{col}{row}'].alignment = left_align
                ws_entities[f'{col}{row}'].border = border
            row += 1

        ws_entities.column_dimensions['A'].width = 50
        ws_entities.column_dimensions['B'].width = 40
        ws_entities.column_dimensions['C'].width = 35

        # Sheet 3: Business Components
        ws_business = wb.create_sheet("Business Components", 2)
        ws_business['A1'] = "Business Components"
        ws_business['A1'].font = title_font
        ws_business['A1'].fill = title_fill
        ws_business.merge_cells('A1:C1')
        
        ws_business['A3'] = "File Path"
        ws_business['B3'] = "Relative Path"
        ws_business['C3'] = "Patterns Found"
        for cell in ['A3', 'B3', 'C3']:
            ws_business[cell].font = header_font
            ws_business[cell].fill = header_fill
            ws_business[cell].alignment = center_align
            ws_business[cell].border = border

        row = 4
        for filepath, patterns in business_components.items():
            relative_path = os.path.relpath(filepath, PROJECT_PATH)
            patterns_str = ', '.join(patterns)
            ws_business[f'A{row}'] = filepath
            ws_business[f'B{row}'] = relative_path
            ws_business[f'C{row}'] = patterns_str
            for col in ['A', 'B', 'C']:
                ws_business[f'{col}{row}'].alignment = left_align
                ws_business[f'{col}{row}'].border = border
            row += 1

        ws_business.column_dimensions['A'].width = 50
        ws_business.column_dimensions['B'].width = 40
        ws_business.column_dimensions['C'].width = 35

        # Sheet 4: JSF Pages
        ws_jsf = wb.create_sheet("JSF Pages", 3)
        ws_jsf['A1'] = "JSF Pages"
        ws_jsf['A1'].font = title_font
        ws_jsf['A1'].fill = title_fill
        ws_jsf.merge_cells('A1:B1')
        
        ws_jsf['A3'] = "File Path"
        ws_jsf['B3'] = "Relative Path"
        for cell in ['A3', 'B3']:
            ws_jsf[cell].font = header_font
            ws_jsf[cell].fill = header_fill
            ws_jsf[cell].alignment = center_align
            ws_jsf[cell].border = border

        row = 4
        for filepath in jsf_pages:
            relative_path = os.path.relpath(filepath, PROJECT_PATH)
            ws_jsf[f'A{row}'] = filepath
            ws_jsf[f'B{row}'] = relative_path
            for col in ['A', 'B']:
                ws_jsf[f'{col}{row}'].alignment = left_align
                ws_jsf[f'{col}{row}'].border = border
            row += 1

        ws_jsf.column_dimensions['A'].width = 50
        ws_jsf.column_dimensions['B'].width = 40

        # Sheet 5: Analysis Log
        ws_log = wb.create_sheet("Analysis Log", 4)
        ws_log['A1'] = "Analysis Log"
        ws_log['A1'].font = title_font
        ws_log['A1'].fill = title_fill
        ws_log.merge_cells('A1:A1')
        
        ws_log['A3'] = analysis_log
        ws_log['A3'].alignment = left_align
        ws_log.column_dimensions['A'].width = 80

        excel_filename = os.path.join(output_path, f"rnc-{folder_name}.xlsx")
        wb.save(excel_filename)
        return excel_filename

    except Exception as e:
        print(f"❌ Erro ao gerar relatório Excel: {e}")
        return None

def generate_markdown_report(output_path):
    """Gera o relatório final em formato Markdown."""
    folder_name = os.path.basename(os.path.abspath(PROJECT_PATH))
    report_filename = os.path.join(output_path, f"rnc-{folder_name}.md")

    report = f"# Relatório de Análise Estática do Projeto: `{folder_name}`\n\n"
    report += f"**Caminho do Projeto:** `{PROJECT_PATH}`\n"
    report += f"**Data da Análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "---\n\n"

    report += "## 1. Classes de Entidades/Objetos de Persistência\n\n"
    report += f"**Total de Classes Encontradas:** **{len(entity_classes)}**\n\n"
    report += "As classes foram identificadas pela presença de anotações JPA/Hibernate comuns (`@Entity`, `@Table`).\n\n"
    report += "```\n"
    for path, patterns in entity_classes.items():
        relative_path = os.path.relpath(path, PROJECT_PATH)
        patterns_str = ', '.join(p for p in patterns)
        report += f"* {relative_path} (Padrão: {patterns_str})\n"
    report += "```\n\n"

    report += "## 2. Classes de Componentes de Negócio/Controladoras/Backing Beans\n\n"
    report += f"**Total de Classes Encontradas:** **{len(business_components)}**\n\n"
    report += "As classes foram identificadas por anotações comuns de injeção/gerenciamento (`@Named`, `@Controller`, etc.).\n\n"
    report += "```\n"
    for path, patterns in business_components.items():
        relative_path = os.path.relpath(path, PROJECT_PATH)
        patterns_str = ', '.join(p for p in patterns)
        report += f"* {relative_path} (Padrão: {patterns_str})\n"
    report += "```\n\n"

    report += "## 3. Páginas JSF (XHTML) Encontradas\n\n"
    report += f"**Total de Páginas Encontradas:** **{len(jsf_pages)}**\n\n"
    report += "(A ligação exata entre a página JSF e a Entidade/Backing Bean é inferida por análise de código.)\n\n"
    report += "```\n"
    for path in jsf_pages:
        relative_path = os.path.relpath(path, PROJECT_PATH)
        report += f"* {relative_path}\n"
    report += "```\n\n"

    report += "## 4. Informações do Banco de Dados (Configurações)\n\n"
    report += "Análise simples de arquivos de configuração comuns:\n\n"
    report += db_info_placeholder
    report += "\n\n"

    report += "## 5. Log de Execução\n\n"
    report += "```\n"
    report += analysis_log
    report += "```\n"

    return report, report_filename

def save_and_display_report(report_content, md_filename, excel_filename=None):
    """Salva os relatórios em Markdown e Excel, e exibe o resumo no terminal."""
    try:
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Relatório Markdown salvo em: {md_filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo Markdown {md_filename}: {e}")

    if excel_filename:
        print(f"✅ Relatório Excel salvo em: {excel_filename}")

    print("\n" + "="*80)
    print("RESUMO DA ANÁLISE ESTATICA")
    print("="*80)
    print(f"Projeto Analisado: {os.path.basename(os.path.abspath(PROJECT_PATH))}")
    print(f"Total de Entidades: {len(entity_classes)}")
    print(f"Total de Componentes de Negócio/Controladoras: {len(business_components)}")
    print(f"Total de Páginas JSF: {len(jsf_pages)}")
    found_db = "Sim" if "Arquivos de Configuração de Banco de Dados Encontrados" in db_info_placeholder else "Não"
    print(f"Informações de DB Encontradas: {found_db}")
    print("="*80)
    print(f"📂 Arquivos de saída estão em: {os.path.dirname(md_filename)}/")
    print("="*80)

# --- Execução Principal ---
if __name__ == "__main__":

    # Requer que o caminho do projeto seja passado como argumento.
    # Se desejar entrada interativa, passe a flag --interactive; caso contrário o script retornará um erro amigável.
    if len(sys.argv) <= 1:
        # Mensagem de erro amigável em texto e JSON para automações
        usage = f"Uso: python {os.path.basename(__file__)} <caminho_para_pasta_projeto>\nExemplo: python {os.path.basename(__file__)} C:\\meu_projeto"
        message_text = (
            "\n🛑 Erro: Pasta do projeto não informada.\n\n"
            f"{usage}\n"
            f"Exemplo: python {os.path.basename(__file__)} C:\\meu_projeto\n\n"
            f"Código de erro: {ERROR_CODE_MISSING_PROJECT}\n"
        )
        print(message_text)
        sys.exit(ERROR_CODE_MISSING_PROJECT)

    PROJECT_PATH = sys.argv[1]
    PROJECT_PATH = os.path.abspath(PROJECT_PATH)

    if not os.path.isdir(PROJECT_PATH):
        print(f"\n🛑 ERRO: O caminho '{PROJECT_PATH}' não é um diretório válido.")
        sys.exit(3)

    # Criar pasta de output dentro do projeto
    output_folder_path = create_output_folder(PROJECT_PATH)

    # Executar análise
    run_analysis(PROJECT_PATH)

    # Gerar relatórios
    report_content, md_filename = generate_markdown_report(output_folder_path)
    excel_filename = generate_excel_report(os.path.basename(os.path.abspath(PROJECT_PATH)), output_folder_path)

    # Salvar e exibir resultados
    save_and_display_report(report_content, md_filename, excel_filename)