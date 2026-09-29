import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <main>
      <h1>Sistema de Cotizaciones</h1>
      <p>Marketing site placeholder — service catalog and lead capture go here.</p>
      <router-outlet />
    </main>
  `,
})
export class AppComponent {}
