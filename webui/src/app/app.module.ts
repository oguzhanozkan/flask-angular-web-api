import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { RssComponent } from './rss/rss.component';
import { RssService } from './rss/rss.service';
import { NgxPaginationModule } from 'ngx-pagination';

import { LoginComponent } from './login/login.component'
import { RegisterComponent } from './register/register.component'
import { HomeComponent } from './home/home.component'
import { FavoriComponent } from './favori/favori.component'
import { AuthenticationService } from './authentication.service'
import { AuthGuardService } from './auth-guard.service'

import { AuthInterceptor } from './auth.interceptor';
import { FavoriService } from './favori/favori.service';
import { SearchComponent } from './search/search.component';
import { SearchService} from './search/search.service';
import { RssDetailComponent } from './rss/rss-detail/rss-detail.component'


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'rss',
    component: RssComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: 'rss/rss-detail/:id',
    component: RssDetailComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: 'favori',
    component: FavoriComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: 'search',
    component: SearchComponent,
    canActivate: [AuthGuardService]
  }
]

@NgModule({
  declarations: [
    AppComponent,
    RssComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    FavoriComponent,
    SearchComponent,
    RssDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    HttpClientModule,
    NgxPaginationModule,
    RouterModule.forRoot(routes)
  ],
  providers: [AuthenticationService,
    AuthGuardService,
    RssService, { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    FavoriService, { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    SearchService, { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
