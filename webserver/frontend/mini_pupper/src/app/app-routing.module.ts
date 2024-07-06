import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PupperComponent } from './components/pupper/pupper.component';
import { SettingsComponent } from './components/settings/settings.component';
import { DanceComponent } from './components/dance/dance.component';
import { WalkComponent } from './components/walk/walk.component';
import { JumpComponent } from './components/jump/jump.component';


const routes: Routes = [
  { path: '', redirectTo: '/pupper', pathMatch: 'full' },
  { path: 'pupper', component: PupperComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'dance', component: DanceComponent },
  { path: 'walk', component: WalkComponent },
  { path: 'jump', component: JumpComponent },];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
