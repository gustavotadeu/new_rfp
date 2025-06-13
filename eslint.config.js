import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    files: ['frontend/**/*.js'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
    },
    rules: {},
  },
  {
    files: ['frontend/__tests__/**/*.js'],
    languageOptions: {
      globals: {
        test: 'readonly',
        expect: 'readonly',
        require: 'readonly',
      },
    },
  },
];
