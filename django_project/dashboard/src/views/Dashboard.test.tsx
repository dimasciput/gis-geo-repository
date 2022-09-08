import React from 'react';
import { render } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders dashboard admin content', () => {
  const { container } = render(
      <Dashboard />
  );
  expect(container.getElementsByClassName(
    'AdminContent').length
  ).toBe(1);
});

test('renders routes', () => {
  const {getAllByText} = render(
    <Dashboard />
  );
  let route = getAllByText('Home');
  expect(route.length > 1).toBeTruthy();
})

