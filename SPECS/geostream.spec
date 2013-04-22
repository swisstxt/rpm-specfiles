Name:           geostream
Version:        0.1.5
Release:        1%{?dist}
Summary:        Geostream - Audiostreaming GEO-IP API
BuildArch:      x86_64
Group:          Application/Internet
License:        commercial
URL:            https://bitbucket.org/swisstxt/geostream
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler
BuildRequires: gcc libxml2 libxml2-devel libxslt libxslt-devel

Requires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler
Requires: libxml2 libxslt

%define git_repo https://niwo@bitbucket.org/swisstxt/%{name}.git
%define appdir /srv/%{name}
%define cfgdir %{appdir}/config
%define logdir %{appdir}/log
%define tmpdir %{appdir}/tmp

%description
Geostream - Audiostreaming GEO-IP API

%prep
rm -rf %{name}
git clone %{git_repo}
pushd %{name}
  git checkout v%{version}
popd

%build
pushd %{name}
  # install all dependencies via bundler
  /opt/ruby-1.9.3/bin/bundle install --deployment --shebang=/opt/ruby-1.9.3/bin/ruby

  # install bundler itself
  cat <<-EOD > gemrc
    gemhome: $PWD/vendor/bundle/ruby/1.9.1
    gempath:
    - $PWD/vendor/bundle/ruby/1.9.1
EOD
  # install all gems using bundler
  /opt/ruby-1.9.3/bin/gem --config-file ./gemrc install bundler
  rm ./gemrc

  # correct shebangs for opt-ruby
  egrep -rl '#!/usr/bin/env ruby' . \
  | xargs sed -ri 's@#!/usr/bin/env ruby@#!/opt/ruby-1.9.3/bin/ruby@g'
  
  egrep -rl '#!/usr/local/bin/ruby' . &&
  egrep -rl '#!/usr/local/bin/ruby' . \
  | xargs sed -ri 's@#!/usr/local/bin/ruby@#!/opt/ruby-1.9.3/bin/ruby@g'

  # precompile assets
  /opt/ruby-1.9.3/bin/bundle exec rake assets:precompile
  # clear tmp
  /opt/ruby-1.9.3/bin/bundle exec rake tmp:clear
  # clear logs
  /opt/ruby-1.9.3/bin/bundle exec rake log:clear
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{tmpdir}

pushd %{name}
  mv * .bundle $RPM_BUILD_ROOT/%{appdir}
popd
rm -f $RPM_BUILD_ROOT/%{appdir}/log/.gitkeep

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{appdir}
%attr(755,geostream,geostream) %{logdir}
%attr(755,geostream,geostream) %{tmpdir}
%doc
