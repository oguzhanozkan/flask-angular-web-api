import { Component } from '@angular/core'
import { AuthenticationService, TokenPayload } from '../authentication.service'
import { Router } from '@angular/router'
import { environment } from 'src/environments/environment'

@Component({
  templateUrl: './login.component.html'
})
export class LoginComponent {
  credentials: TokenPayload = {
    _id: '',
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  }

  constructor(private auth: AuthenticationService, private router: Router) {}

  login() {
    this.auth.login(this.credentials).subscribe(
      () => {
        this.router.navigateByUrl('rss')
      },
      err => {
        console.error(err)
      }
    )
  }
}
