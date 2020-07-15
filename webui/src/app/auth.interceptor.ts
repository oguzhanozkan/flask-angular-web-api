import {HttpInterceptor, HttpHandler, HttpRequest} from '@angular/common/http';
import {tap} from 'rxjs/operators'

export class AuthInterceptor implements HttpInterceptor{
    
    intercept(req: HttpRequest<any>, next: HttpHandler){

        const token = localStorage.getItem('usertoken');

        const newReq = req.clone({
            headers: req.headers.set(
                'Authorization', 'Bearer ' + token
            )
        });

        //console.log(token)

        return next.handle(newReq).pipe(
            tap(succ => console.log(succ),
            err => console.log(err))
        );
    }
}