const fs = require('fs');

test('project page exists', () => {
  expect(fs.existsSync('project.html')).toBe(true);
});
