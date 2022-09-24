import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PupperComponent } from './pupper.component';

describe('PupperComponent', () => {
  let component: PupperComponent;
  let fixture: ComponentFixture<PupperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PupperComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PupperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
