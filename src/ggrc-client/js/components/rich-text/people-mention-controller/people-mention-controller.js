/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './people-mention-controller.stache';

const MENTION_REGEX = /(^.*[\s]|^)[@+]([\S]*)$/s;

/**
 * Supporting component for rich-text to handle mentions of people
 */
export default can.Component.extend({
  tag: 'people-mention-controller',
  template,
  leakScope: false,
  viewModel: {
    define: {
      editor: {
        set(editor) {
          if (editor) {
            editor.on('text-change', this.onChange.bind(this));
          }
          return editor;
        },
      },
    },
    mentionValue: null,
    mentionIndex: null,
    onChange() {
      const editor = this.attr('editor');
      const selection = editor.getSelection();
      if (!selection) {
        // on mention insert focus is lost
        return;
      }
      const selectionIndex = selection.index;
      const editorText = editor.getText();
      const textBeforeSelection = editorText.substring(0, selectionIndex);

      const groups = MENTION_REGEX.exec(textBeforeSelection);
      if (groups) {
        const textBeforeMention = groups[1];
        const mentionValue = groups[2];

        this.attr('mentionValue', mentionValue);
        this.attr('mentionIndex', textBeforeMention.length);
      } else {
        this.attr('mentionValue', null);
        this.attr('mentionIndex', null);
      }
    },
  },
});
