t=100
x=1:1:t
y=factorial(t)./factorial(x)./factorial(t-x).*0.2.^x.*0.8.^(t-x)
plot(x,y)

