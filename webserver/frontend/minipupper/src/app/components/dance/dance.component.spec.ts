import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DanceComponent } from './dance.component';

describe('DanceComponent', () => {
  let component: DanceComponent;
  let fixture: ComponentFixture<DanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DanceComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
