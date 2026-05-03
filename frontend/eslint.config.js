import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import prettierConfig from 'eslint-config-prettier'
import unusedImports from 'eslint-plugin-unused-imports'

export default tseslint.config(
  { ignores: ['dist/**', 'node_modules/**'] },

  // Vue-парсер для .vue файлов
  ...pluginVue.configs['flat/recommended'],

  // TypeScript правила только для .ts (чтобы не перекрывать vue-eslint-parser)
  ...tseslint.configs.recommended.map((config) => ({
    ...config,
    files: ['**/*.ts'],
  })),

  // TypeScript в <script> блоках .vue через parserOptions
  {
    files: ['**/*.vue'],
    plugins: { '@typescript-eslint': tseslint.plugin },
    languageOptions: {
      parserOptions: { parser: tseslint.parser },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      // no-unused-vars отключён для .vue: TS-парсер не видит использование переменных
      // в шаблоне — давал бы ложные срабатывания на reactive refs.
      // Неиспользуемые переменные в скрипте ловит tsconfig noUnusedLocals.
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },

  // Автоудаление неиспользуемых импортов для .ts файлов
  {
    files: ['**/*.ts'],
    plugins: { 'unused-imports': unusedImports },
    rules: {
      '@typescript-eslint/no-unused-vars': 'off',
      'unused-imports/no-unused-imports': 'error',
      'unused-imports/no-unused-vars': [
        'warn',
        { vars: 'all', varsIgnorePattern: '^_', args: 'after-used', argsIgnorePattern: '^_' },
      ],
    },
  },

  prettierConfig,

  {
    rules: {
      'vue/multi-word-component-names': 'off',
      // с TypeScript props типизируются через интерфейс — default value не нужен
      'vue/require-default-prop': 'off',
    },
  },
)
