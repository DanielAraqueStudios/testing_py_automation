import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'platform-button',
  standalone: true,
  imports: [CommonModule],
  template: `<button [type]="type" [disabled]="disabled"><ng-content></ng-content></button>`,
})
export class ButtonComponent {
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() disabled = false;
}
