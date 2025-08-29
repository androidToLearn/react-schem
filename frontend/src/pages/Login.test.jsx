import Login from "./LoginPage";
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';



test('login', async () => {
    //success login page test
    const { container } = render(<MemoryRouter><Login /></MemoryRouter>);
    await waitFor(() => {
        expect(container.querySelector('.btnContainer')).toBeInTheDocument();
        console.log('הפרטים מופיעים בעמוד Login')
    });

});

test('loginFailing', async () => {
    //failed login page test
    const { container } = render(<MemoryRouter><Login /></MemoryRouter>);

    await waitFor(() => {
        let p1 = container.querySelector('.p1')

        if (!p1) {
            console.log('טקסט p1 לא מופיע בlogin page')
        }
    });


});