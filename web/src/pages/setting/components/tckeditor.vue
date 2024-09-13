<template>
  <t-dialog :header="false" :visible="visible" :width="1200" :footer="false" :onClose="on_dialog_close">
    <div class="editor-container editor-container_classic-editor" ref="editorContainerElement">
      <div class="editor-container__editor">
        <div ref="editorElement" style="height: 500px;overflow-y: scroll;">
          <ckeditor v-if="isLayoutReady" v-model="text_content" :editor="editor" :config="config" />
        </div>
      </div>
    </div>
  </t-dialog>
</template>

<script>


import {
  ClassicEditor,
  AccessibilityHelp,
  Autoformat,
  AutoLink,
  Autosave,
  Bold,
  Code,
  CodeBlock,
  Essentials,
  FindAndReplace,
  FontBackgroundColor,
  FontColor,
  FontFamily,
  FontSize,
  FullPage,
  GeneralHtmlSupport,
  Heading,
  Highlight,
  HtmlComment,
  HtmlEmbed,
  Italic,
  Link,
  Paragraph,
  RemoveFormat,
  SelectAll,
  ShowBlocks,
  SourceEditing,
  SpecialCharacters,
  SpecialCharactersArrows,
  SpecialCharactersCurrency,
  SpecialCharactersEssentials,
  SpecialCharactersLatin,
  SpecialCharactersMathematical,
  SpecialCharactersText,
  Strikethrough,
  Subscript,
  Superscript,
  Table,
  TableCaption,
  TableCellProperties,
  TableColumnResize,
  TableProperties,
  TableToolbar,
  TextTransformation,
  Underline,
  Undo
} from 'ckeditor5';
import translations from 'ckeditor5/translations/zh-cn.js';
import 'ckeditor5/ckeditor5.css';

export default {
  name: 'Tckeditor',
  props:{show:Boolean,content:String},
  data() {
    return {
      visible:false,
      isLayoutReady: false,
      config: null,
      text_content:"",
      editor: ClassicEditor
    };
  },
  watch: {
    show: {
      handler(nval) {
        if(nval){
          this.visible = true;
          this.text_content = this.content;
        }
      },
    }
  },
  mounted() {
    this.config = {
      toolbar: {
        items: [
          'undo',
          'redo',
          '|',
          'sourceEditing',
          'showBlocks',
          'findAndReplace',
          '|',
          'heading',
          '|',
          'fontSize',
          'fontFamily',
          'fontColor',
          'fontBackgroundColor',
          '|',
          'bold',
          'italic',
          'underline',
          'strikethrough',
          'subscript',
          'superscript',
          'code',
          'removeFormat',
          '|',
          'specialCharacters',
          'link',
          'insertTable',
          'highlight',
        ],
        shouldNotGroupWhenFull: true
      },
      plugins: [
        AccessibilityHelp,
        Autoformat,
        AutoLink,
        Autosave,
        Bold,
        Code,
        CodeBlock,
        Essentials,
        FindAndReplace,
        FontBackgroundColor,
        FontColor,
        FontFamily,
        FontSize,
        FullPage,
        GeneralHtmlSupport,
        Heading,
        Highlight,
        HtmlComment,
        HtmlEmbed,
        Italic,
        Link,
        Paragraph,
        RemoveFormat,
        SelectAll,
        ShowBlocks,
        SourceEditing,
        SpecialCharacters,
        SpecialCharactersArrows,
        SpecialCharactersCurrency,
        SpecialCharactersEssentials,
        SpecialCharactersLatin,
        SpecialCharactersMathematical,
        SpecialCharactersText,
        Strikethrough,
        Subscript,
        Superscript,
        Table,
        TableCaption,
        TableCellProperties,
        TableColumnResize,
        TableProperties,
        TableToolbar,
        TextTransformation,
        Underline,
        Undo
      ],
      fontFamily: {
        supportAllValues: true
      },
      fontSize: {
        options: [10, 12, 14, 'default', 18, 20, 22],
        supportAllValues: true
      },
      heading: {
        options: [
          {
            model: 'paragraph',
            title: 'Paragraph',
            class: 'ck-heading_paragraph'
          },
          {
            model: 'heading1',
            view: 'h1',
            title: 'Heading 1',
            class: 'ck-heading_heading1'
          },
          {
            model: 'heading2',
            view: 'h2',
            title: 'Heading 2',
            class: 'ck-heading_heading2'
          },
          {
            model: 'heading3',
            view: 'h3',
            title: 'Heading 3',
            class: 'ck-heading_heading3'
          },
          {
            model: 'heading4',
            view: 'h4',
            title: 'Heading 4',
            class: 'ck-heading_heading4'
          },
          {
            model: 'heading5',
            view: 'h5',
            title: 'Heading 5',
            class: 'ck-heading_heading5'
          },
          {
            model: 'heading6',
            view: 'h6',
            title: 'Heading 6',
            class: 'ck-heading_heading6'
          }
        ]
      },
      htmlSupport: {
        allow: [
          {
            name: /^.*$/,
            styles: true,
            attributes: true,
            classes: true
          }
        ]
      },
      initialData:'',
      language: 'zh-cn',
      link: {
        addTargetToExternalLinks: true,
        defaultProtocol: 'https://',
        decorators: {
          toggleDownloadable: {
            mode: 'manual',
            label: 'Downloadable',
            attributes: {
              download: 'file'
            }
          }
        }
      },
      placeholder: '',
      table: {
        contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
      },
      translations: [translations]
    };
    this.isLayoutReady = true;
  },
  methods:{
    on_dialog_close(){
      this.$emit("onClose",this.text_content);
      this.visible = false;
    }
  }
};
</script>
