# Mobile apps are not normally containerised — you build an APK or IPA instead.
# This Dockerfile builds the WEB version of the Flutter app, which is useful
# for a quick hosted demo.
FROM ghcr.io/cirruslabs/flutter:stable AS build
WORKDIR /app
COPY pubspec.* ./
RUN flutter pub get
COPY . .
RUN flutter build web --release

FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html
EXPOSE 80
