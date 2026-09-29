import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <main>
      <h1>Client Portal</h1>
      <p>Dashboard placeholder — project progress and live chat go here.</p>
      <router-outlet />
    </main>
  `,
})
export class AppComponent {}
