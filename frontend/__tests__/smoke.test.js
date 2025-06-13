const fs = require('fs');
test('login and register pages exist', () => {
  expect(fs.existsSync('login.html')).toBe(true);
  expect(fs.existsSync('register.html')).toBe(true);
});
