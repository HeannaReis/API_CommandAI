from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from config.config import Config
import os
from core.logger_config import logger  # Importação correta

class DocumentService:
    def __init__(self):
        self.doc = self._load_or_create_document()
        self._setup_document_styles()

    def _load_or_create_document(self):
        if os.path.exists(Config.OUTPUT_DOCX):
            return Document(Config.OUTPUT_DOCX)
        doc = Document()
        # Configuração inicial do documento
        title = doc.add_heading('Análise de Imagens com Inteligência Artificial', level=0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Adiciona subtítulo
        subtitle = doc.add_paragraph('Relatório Gerado Automaticamente')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.style = 'Subtitle'

        # Adiciona uma quebra de página após o título
        doc.add_page_break()

        return doc

    def _setup_document_styles(self):
        """Configura estilos personalizados para o documento"""
        styles = self.doc.styles

        # Estilo para título de imagem
        if 'Image Title' not in styles:
            image_title_style = styles.add_style('Image Title', WD_STYLE_TYPE.PARAGRAPH)
            font = image_title_style.font
            font.name = 'Calibri'
            font.size = Pt(16)
            font.bold = True
            font.color.rgb = RGBColor(0, 112, 192)  # Azul
            paragraph_format = image_title_style.paragraph_format
            paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER  # Centraliza o título
            paragraph_format.space_before = Pt(12)
            paragraph_format.space_after = Pt(6)

        # Estilo para o texto do resumo
        if 'Summary Text' not in styles:
            summary_style = styles.add_style('Summary Text', WD_STYLE_TYPE.PARAGRAPH)
            font = summary_style.font
            font.name = 'Calibri'
            font.size = Pt(11)
            paragraph_format = summary_style.paragraph_format
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            paragraph_format.space_before = Pt(0)  # Reduzir o espaçamento antes do resumo
            paragraph_format.space_after = Pt(12)
            paragraph_format.first_line_indent = Pt(18)  # Recuo na primeira linha

    def add_image_summary(self, image_name, summary):
        image_path = os.path.join(Config.PROCESSED_DIR, image_name)
        logger.info(f"Caminho da imagem para o Word: {image_path}")  # Uso correto do logger

        # Adiciona o título da imagem
        p = self.doc.add_paragraph(image_name, style='Image Title')  # Adiciona o título antes da imagem


        # Adiciona a imagem ao documento com tamanho de página inteira
        if os.path.exists(image_path):
            paragraph = self.doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run()

            # Obtém a largura da página
            section = self.doc.sections[0]
            page_width = section.page_width
            page_height = section.page_height

            # Calcula as margens
            left_margin = section.left_margin
            right_margin = section.right_margin

            # Calcula a largura disponível (largura da página menos margens)
            available_width = page_width - left_margin - right_margin

            # Adiciona a imagem com a largura disponível
            picture = run.add_picture(image_path, width=available_width)

            # Remover a linha que adiciona o parágrafo vazio
            # self.doc.add_paragraph()

        # Formata o resumo com estilo personalizado
        clean_summary = self._clean_markdown(summary)

        # Adiciona o resumo com estilo personalizado
        p = self.doc.add_paragraph(clean_summary, style='Summary Text')

    def _add_horizontal_line(self):
        """Adiciona uma linha horizontal decorativa"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fmt = p.paragraph_format
        p_fmt.space_after = Pt(12)

        # Adiciona uma linha usando caracteres
        run = p.add_run('─' * 50)  # 50 caracteres de linha
        run.font.color.rgb = RGBColor(192, 192, 192)  # Cinza claro

    def _clean_markdown(self, text):
        """Remove marcações markdown do texto"""
        # Remove cabeçalhos markdown (###, ##, etc)
        import re
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Remove marcações de negrito e itálico
        text = text.replace('**', '').replace('*', '').replace('__', '').replace('_', '')

        # Remove marcadores de lista
        text = re.sub(r'^\s*[-*+]\s+', '• ', text, flags=re.MULTILINE)

        return text

    def save_document(self):
        # Adiciona informações de rodapé
        # section = self.doc.sections[0]
        # footer = section.footer
        # footer_para = footer.paragraphs[0]
        # footer_para.text = f"Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Assistente Visual Inteligente"
        # footer_para.style = self.doc.styles['Footer']

        self.doc.save(Config.OUTPUT_DOCX)